import argparse
import json
import re
from json import JSONDecodeError

from datasets import load_from_disk
from tqdm import tqdm

from experiment.agent.experiment_agent import ExpirementAgent
from aios.utils.utils import parse_global_args
from aios.hooks.llm import aios_starter
from experiment.agent.interpreter import InterpreterAgent
from pyopenagi.agents.agent_process import AgentProcessFactory

AGENT_TYPE_MAPPING_AIOS = {
    "interpreter": InterpreterAgent,
}


def parse_patch(agent_result: str):
    pattern = r'```patch\s*([\s\S]*?)```'

    match = re.search(pattern, agent_result)

    if match:
        patch = match.group(1)
        return patch
    else:
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
    except FileNotFoundError or JSONDecodeError:
        predictions = []

    predictions.append(prediction)

    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(predictions, file, ensure_ascii=False, indent=4)

    print(f"Write prediction: {prediction}")


def creat_agent(process_factory: AgentProcessFactory, agent_type: str) -> ExpirementAgent:
    agent = AGENT_TYPE_MAPPING_AIOS[agent_type](process_factory)
    return agent


def run_swe_bench(agent: ExpirementAgent, single_data) -> str:
    input_str = single_data["text"]
    result = agent.run(input_str)
    return parse_patch(result)


def main(agent_type: str, data_path: str, out_path: str, on_aios: bool, args):
    dataset = load_from_disk(data_path)
    test_data = dataset["test"]

    if on_aios:
        process_factory = AgentProcessFactory()
        with aios_starter(**vars(args)):
            for data in tqdm(test_data):
                agent = creat_agent(process_factory, agent_type)
                patch = run_swe_bench(agent, data)
                write_prediction(data["instance_id"], patch, agent_type, out_path)
    else:
        pass


if __name__ == '__main__':
    parser = parse_global_args()

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("--agent_type", type=str, default="interpreter")
    main_parser.add_argument("--data_path", type=str, default="dataset/SWE-bench__style-3__fs-oracle")
    main_parser.add_argument("--out_path", type=str, default="prediction.json")
    main_parser.add_argument("--on_aios", action="store_true")

    global_args, remaining_args = parser.parse_known_args()
    main_args = main_parser.parse_args(remaining_args)

    main(**vars(main_args), args=global_args)
