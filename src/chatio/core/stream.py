
from abc import ABC, abstractmethod

from collections.abc import Iterator

from types import TracebackType

from .events import ChatEvent


class ApiStream(ABC):

    @abstractmethod
    def __enter__(self) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...
