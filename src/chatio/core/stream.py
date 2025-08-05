
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .object import Closeable

from .events import ChatEvent


class ApiStream(Closeable, ABC):

    @abstractmethod
    def __iter__(self) -> Iterator[ChatEvent]:
        ...
