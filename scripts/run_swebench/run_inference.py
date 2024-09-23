import json
import os.path

from aios.utils.utils import (
    parse_global_args,
)

import warnings

from aios.hooks.llm import useFactory, useKernel, useFIFOScheduler

from aios.utils.utils import delete_directories
from dotenv import load_dotenv
from datasets import load_from_disk

def clean_cache(root_directory):
    targets = {
        ".ipynb_checkpoints",
        "__pycache__",
        ".pytest_cache",
        "context_restoration",
    }
    delete_directories(root_directory, targets)

def inference_core(input_path, out_path, submitAgent, awaitAgentExecution):
    text_data = load_from_disk(input_path)
    text_data_test = text_data["test"]

    run_round = min(len(text_data_test), 2)
    agent_ids = []
    for i in range(run_round):
        instance_id = text_data_test[i]["instance_id"]
        text = text_data_test[i]["text"]

        agent_id = submitAgent(
            agent_name="experiment/doraemon_agent",
            task_input=text
        )

        agent_ids.append({"agent_id": agent_id, "instance_id": instance_id})

    predictions = []
    count = 0
    for id_pair in agent_ids:
        agent_id = id_pair["agent_id"]
        instance_id = id_pair["instance_id"]

        result = awaitAgentExecution(agent_id)

        prediction = {
            "instance_id": instance_id,
            "model_patch": result["result"],
            "model_name_or_path": "doraemon_agent"
        }

        count += 1
        print(f"Prediction complete: {count}/{run_round}")
        predictions.append(prediction)

    with open(os.path.join(out_path, "predictions.json"), "w", encoding="utf-8") as file:
        json.dump(predictions, file, ensure_ascii=False, indent=4)

def main(input_path, out_path):
    # parse arguments and set configuration for this run accordingly
    warnings.filterwarnings("ignore")
    parser = parse_global_args()
    args = parser.parse_args()

    llm_name = args.llm_name
    max_gpu_memory = args.max_gpu_memory
    eval_device = args.eval_device
    max_new_tokens = args.max_new_tokens
    scheduler_log_mode = args.scheduler_log_mode
    agent_log_mode = args.agent_log_mode
    llm_kernel_log_mode = args.llm_kernel_log_mode
    use_backend = args.use_backend
    load_dotenv()

    llm = useKernel(
        llm_name=llm_name,
        max_gpu_memory=max_gpu_memory,
        eval_device=eval_device,
        max_new_tokens=max_new_tokens,
        log_mode=llm_kernel_log_mode,
        use_backend=use_backend
    )

    # run agents concurrently for maximum efficiency using a scheduler
    startScheduler, stopScheduler = useFIFOScheduler(
        llm=llm,
        log_mode=scheduler_log_mode,
        get_queue_message=None
    )
    submitAgent, awaitAgentExecution = useFactory(
        log_mode=agent_log_mode,
        max_workers=500
    )

    startScheduler()

    inference_core(input_path, out_path, submitAgent, awaitAgentExecution)

    stopScheduler()

    clean_cache(root_directory="./")


if __name__ == "__main__":
    INPUT_PATH = "/Users/mujian/home/code/python/AIOS/pyopenagi/data/swebench/text_data/SWE-bench__style-3__fs-oracle"
    OUT_PATH = "/Users/mujian/home/code/python/AIOS/pyopenagi/data/swebench/"
    main(INPUT_PATH, OUT_PATH)
