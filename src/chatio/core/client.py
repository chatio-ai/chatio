
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .params import ApiParams
from .events import ChatEvent


class ApiClient(ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, params: ApiParams) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(self, model: str, params: ApiParams) -> int:
        ...
