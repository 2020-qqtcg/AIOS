from typing import Any

from pydantic.v1 import BaseModel
from tqdm import tqdm

from aios.utils.logger import SDKLogger
from experiment.agent.autogen import AutoGenAgent
from experiment.agent.experiment_agent import SimpleLLMAgent
from experiment.agent.interpreter import InterpreterAgent
from experiment.agent.metagpt import MetaGPTAgent

AGENT_TYPE_MAPPING_AIOS = {
    "interpreter": InterpreterAgent,
    "gpt": SimpleLLMAgent,
    "metagpt": MetaGPTAgent,
    "autogen": AutoGenAgent,
}

logger = SDKLogger("Experiment")


class MetaData(BaseModel):
    dataset: Any
    split: str = None
    agent_type: str
    output_file: str
    on_aios: bool = True
    max_num: int = None
    aios_args: dict


def run(process_one_func, meta_data: MetaData, write_output_func=None):
    total_result = []
    if meta_data.split:
        dataset = meta_data.dataset[meta_data.split]
    else:
        dataset = meta_data.dataset

    for data in tqdm(dataset):
        if meta_data.max_num is not None:
            if meta_data.max_num > 0:
                meta_data.max_num -= 1
            else:
                logger.log(f"Max num {meta_data.max_num} reached", level="info")
                break

        result = process_one_func(data, meta_data)
        total_result.append(result)

    if write_output_func:
        write_output_func(total_result, meta_data.output_file)
    return total_result