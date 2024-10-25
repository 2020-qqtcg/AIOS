import argparse
import json
import re
from json import JSONDecodeError
from typing import List

from datasets import load_dataset

from aios.hooks.llm import aios_starter
from aios.utils.utils import parse_global_args
from experiment.agent.experiment_agent import ExpirementAgent
from experiment.experiment_core import MetaData, run, AGENT_TYPE_MAPPING_AIOS, logger


def parse_patch(agent_result: str):
    patterns = [r'```patch\s*([\s\S]*?)```', r'```diff\s*([\s\S]*?)```', r'<patch>(.*?)</patch>']

    for pattern in patterns:
        match = re.search(pattern, agent_result)
        if match:
            patch = match.group(1)
            return patch

    try:
        with open("wrong_result.json", "r", encoding="utf-8") as file:
            predictions = json.load(file)
    except FileNotFoundError:
        predictions = []
    except JSONDecodeError:
        predictions = []

    predictions.append(agent_result)
    with open("wrong_result.json", "w", encoding="utf-8") as file:
        json.dump(predictions, file, ensure_ascii=False, indent=4)

    return "[None]"


def write_prediction(instance_id: str, model_patch: str, model_name_or_path: str, out_path: str):
    prediction = {
        "instance_id": instance_id,
        "model_patch": model_patch,
        "model_name_or_path": model_name_or_path,
    }

    try:
        with open(out_path, "r", encoding="utf-8") as file:
            predictions = json.load(file)
    except FileNotFoundError:
        predictions = []
    except JSONDecodeError:
        predictions = []

    predictions.append(prediction)

    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(predictions, file, ensure_ascii=False, indent=4)

    print(f"Write prediction: {prediction}")


def write_result(result_list: List, output_file: str):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result_list, file, ensure_ascii=False, indent=4)
    logger.log(f"Write results num: {len(result_list)}", level="info")


def process_one_func(data, meta_data: MetaData):
    with aios_starter(**meta_data.aios_args):
        agent: ExpirementAgent = AGENT_TYPE_MAPPING_AIOS[meta_data.agent_type](meta_data.on_aios)
        input_str = data["text"]
        result = agent.run(input_str)
        patch = parse_patch(result)

        prediction = {
            "instance_id": data["instance_id"],
            "model_patch": patch,
            "model_name_or_path": meta_data.agent_type,
        }
    return prediction


def run_inference(
        agent_type: str,
        data_name: str,
        split: str,
        output_file: str,
        on_aios: bool,
        max_num: int,
        aios_args: dict):
    dataset = load_dataset(data_name, split=split)

    meta_data = MetaData(
        dataset=dataset,
        agent_type=agent_type,
        output_file=output_file,
        on_aios=on_aios,
        max_num=max_num,
        aios_args=aios_args,
    )

    run(
        process_one_func=process_one_func,
        meta_data=meta_data,
        write_output_func=write_result,
    )


if __name__ == '__main__':
    parser = parse_global_args()

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("--agent_type", type=str, default="interpreter")
    main_parser.add_argument("--data_name", type=str, default="princeton-nlp/SWE-bench_Lite_oracle")
    main_parser.add_argument("--split", type=str, default="test")
    main_parser.add_argument("--output_file", type=str, default="prediction.json")
    main_parser.add_argument("--on_aios", action="store_true")
    main_parser.add_argument("--max_num", type=int, default=None)

    global_args, remaining_args = parser.parse_known_args()
    main_args = main_parser.parse_args(remaining_args)

    run_inference(
        agent_type=main_args.agent_type,
        data_name=main_args.data_name,
        split=main_args.split,
        output_file=main_args.output_file,
        on_aios=main_args.on_aios,
        max_num=main_args.max_num,
        aios_args=vars(global_args)
    )
