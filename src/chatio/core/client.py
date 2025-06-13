
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .events import ChatEvent


class ChatClient[SystemContent, MessageContent, ToolDefinition](ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, system: SystemContent | None,
                             messages: list[MessageContent],
                             tools: list[ToolDefinition] | None) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(self, model: str, system: SystemContent | None,
                             messages: list[MessageContent],
                             tools: list[ToolDefinition] | None) -> int:
        ...
