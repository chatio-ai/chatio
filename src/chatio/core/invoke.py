
from abc import ABC, abstractmethod

from collections.abc import AsyncIterator

from typing import Any

from chatio.core.schema import ToolSchemaDict


class ToolBase(ABC):

    @staticmethod
    @abstractmethod
    def schema() -> ToolSchemaDict:
        ...

    @abstractmethod
    def __call__(self, *_args: Any, **_kwargs: Any) -> AsyncIterator[str | dict]:    # noqa: ANN401
        ...
