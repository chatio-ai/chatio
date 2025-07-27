
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .models import ChatState
from .models import ChatTools
from .events import ChatEvent


class ApiClient(ABC):

    @abstractmethod
    def iterate_model_events(
            self, model: str, state: ChatState, tools: ChatTools) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
