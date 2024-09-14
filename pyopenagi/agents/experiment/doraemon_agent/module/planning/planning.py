from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

from pyopenagi.utils.logger import AgentLogger


class Planning(ABC, BaseModel):

    name: str

    @abstractmethod
    def plan(self, agent, logger: AgentLogger) -> Any:
        """Use plan straregy execute agent

        Args:
            agent: agent executing
            logger: logger to log

        Returns: plan result

        """
        pass
