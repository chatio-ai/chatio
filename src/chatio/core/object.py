
from abc import ABC, abstractmethod

from types import TracebackType

from typing import Protocol
from typing import Self


class Closeable(ABC):

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return await self.close()

    @abstractmethod
    async def close(self) -> None:
        ...


class SupportsCloseable(Protocol):

    async def __aenter__(self) -> Self:
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...

    async def close(self) -> None:
        ...
