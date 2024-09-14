from abc import ABC, abstractmethod
from typing import Any

from pyopenagi.utils.chat_template import Response


class Action(ABC):

    @abstractmethod
    def run(self, response: Response) -> Any:
        pass
