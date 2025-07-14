
from abc import ABC, abstractmethod

from collections.abc import AsyncIterator

from .object import Closeable

from .events import ChatEvent


class ApiStream(Closeable, ABC):

    @abstractmethod
    def __aiter__(self) -> AsyncIterator[ChatEvent]:
        ...
