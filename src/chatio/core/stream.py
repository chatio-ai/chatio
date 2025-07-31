
from abc import ABC, abstractmethod

from collections.abc import Iterator

from types import TracebackType

from typing import Self

from .events import ChatEvent


class ApiStream(ABC):

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return self.close()

    @abstractmethod
    def __iter__(self) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
