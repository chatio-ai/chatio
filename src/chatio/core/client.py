
from abc import ABC, abstractmethod

from .models import ChatState
from .models import ChatTools
from .stream import ApiStream


class ApiClient(ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        ...

    @abstractmethod
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
