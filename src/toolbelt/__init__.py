
from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class ToolBase(ABC):

    @staticmethod
    @abstractmethod
    def schema() -> dict[str, object]:
        ...
