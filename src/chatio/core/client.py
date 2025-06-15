
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .events import ChatEvent


class ChatClient[
    SystemContent,
    MessageContent,
    ToolDefinitions,
](ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, system: SystemContent | None,
                             messages: list[MessageContent],
                             tools: ToolDefinitions | None) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(self, model: str, system: SystemContent | None,
                             messages: list[MessageContent],
                             tools: ToolDefinitions | None) -> int:
        ...
