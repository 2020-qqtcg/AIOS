import argparse
import json
from contextlib import contextmanager

from datasets import load_from_disk
from tqdm import tqdm

from expirement.agent.experiment_agent import ExpirementAgent
from aios.utils.utils import parse_global_args
from aios.hooks.llm import useKernel, fifo_scheduler
from expirement.agent.interpreter import InterpreterAgent
from pyopenagi.agents.agent_process import AgentProcessFactory

AGENT_TYPE_MAPPING = {
    "interpreter": InterpreterAgent,
}


@contextmanager
def aiso_context():
    parser = parse_global_args()
    args = parser.parse_args()

    llm = useKernel(
        llm_name=args.llm_name,
        max_gpu_memory=args.max_gpu_memory,
        eval_device=args.eval_device,
        max_new_tokens=args.max_new_tokens,
        log_mode=args.llm_kernel_log_mode,
        use_backend=args.use_backend
    )

    with fifo_scheduler(llm=llm, log_mode=args.scheduler_log_mode, get_queue_message=None):
        yield


def parse_patch(agent_result: str):
    return agent_result


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

    predictions.append(prediction)

    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(predictions, file, ensure_ascii=False, indent=4)

    print(f"Write prediction: {prediction}")


def creat_agent(process_factory: AgentProcessFactory, agent_type: str) -> ExpirementAgent:
    agent = AGENT_TYPE_MAPPING[agent_type](process_factory)
    return agent


def run_swe_bench(agent: ExpirementAgent, single_data) -> str:
    input_str = single_data["text"]
    result = agent.run(input_str)
    return parse_patch(result)


def main(agent_type: str, data_path: str, out_path: str):
    dataset = load_from_disk(data_path)
    test_data = dataset["test"]
    process_factory = AgentProcessFactory()
    with aiso_context():
        for data in tqdm(test_data):
            agent = creat_agent(process_factory, agent_type)
            patch = run_swe_bench(agent, data)
            write_prediction(data["instance_id"], patch, agent_type, out_path)


if __name__ == '__main__':
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("--agent_type", type=str, default="interpreter")
    main_parser.add_argument("--data_path", type=str, default="dataset")
    main_parser.add_argument("--out_path", type=str, default="prediction.json")
    main_args = main_parser.parse_args()

    main(**vars(main_args))
