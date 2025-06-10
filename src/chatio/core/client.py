
from abc import ABC, abstractmethod

from collections.abc import Iterator


from .events import ChatEvent


class ChatClient(ABC):

    @abstractmethod
    def iterate_model_events(self, model, system, messages, tools) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(self, model, system, messages, tools) -> int:
        ...
