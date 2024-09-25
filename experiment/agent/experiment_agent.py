from abc import ABC, abstractmethod


class ExpirementAgent(ABC):

    @abstractmethod
    def run(self, input_str: str):
        pass
