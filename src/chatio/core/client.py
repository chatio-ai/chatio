
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .params import ApiStates
from .events import ChatEvent


class ApiClient(ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, states: ApiStates) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(self, model: str, states: ApiStates) -> int:
        ...
