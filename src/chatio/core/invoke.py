
from abc import ABC, abstractmethod

from collections.abc import Iterator

from typing import Any

from chatio.core.schema import ToolSchemaDict


# pylint: disable=too-few-public-methods
class ToolBase(ABC):

    @staticmethod
    @abstractmethod
    def schema() -> ToolSchemaDict:
        ...

    @abstractmethod
    def __call__(self, *_args: Any, **_kwargs: Any) -> Iterator[str | dict]:    # noqa: ANN401
        ...
