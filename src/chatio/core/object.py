
from abc import ABC, abstractmethod

from types import TracebackType

from typing import Self


class Closeable(ABC):

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
    def close(self) -> None:
        ...
