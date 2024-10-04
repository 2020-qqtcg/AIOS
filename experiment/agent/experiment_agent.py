from abc import ABC, abstractmethod

from pyopenagi.agents.call_core import CallCore
from pyopenagi.utils.chat_template import Query


class ExpirementAgent(ABC):

    @abstractmethod
    def run(self, input_str: str):
        pass


class SimpleLLMAgent(ExpirementAgent, CallCore):

    def __init__(self, agent_process_factory):
        super().__init__("gpt-4o", agent_process_factory)

    def run(self, input_str: str):
        message = {"content": input_str, "role": "user"}
        query = Query(messages=[message], tools=None)

        response, _, _, _, _ = self.get_response(query)
        result = response.response_message
        return result
