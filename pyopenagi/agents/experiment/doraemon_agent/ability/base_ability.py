from abc import ABC, abstractmethod

from pyopenagi.utils.logger import AgentLogger


class BaseAbility(ABC):

    def __init__(
            self,
            ability_name: str | None = None,
            log_mode: str = "console",
    ):
        self.ability_name = ability_name
        self.logger = AgentLogger(logger_name=ability_name, log_mode=log_mode)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
