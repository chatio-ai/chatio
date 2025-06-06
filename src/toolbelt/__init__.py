
from abc import ABC, abstractmethod


class ToolBase(ABC):

    @staticmethod
    @abstractmethod
    def desc() -> str:
        ...

    @staticmethod
    @abstractmethod
    def schema() -> dict[str, object]:
        ...
