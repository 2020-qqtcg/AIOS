from abc import ABC, abstractmethod
from typing import Any

from pyopenagi.agents.base_agent import BaseAgent


class Planning(ABC):

    @abstractmethod
    def plan(self, agent: BaseAgent) -> Any:
        """Use plan straregy execute agent

        Args:
            agent: agent executing

        Returns: plan result

        """
        pass
