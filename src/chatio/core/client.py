
from abc import ABC, abstractmethod

from collections.abc import Iterator

from .kwargs import ChatKwargs
from .events import ChatEvent


class ChatClient[
    SystemContent,
    MessageContent,
    PredictionContent,
    ToolDefinitions,
    ToolSelection,
](ABC):

    @abstractmethod
    def iterate_model_events(
        self, model: str,
        state: ChatKwargs[
            SystemContent,
            MessageContent,
            PredictionContent,
            ToolDefinitions,
            ToolSelection,
        ],
    ) -> Iterator[ChatEvent]:
        ...

    @abstractmethod
    def count_message_tokens(
        self, model: str,
        state: ChatKwargs[
            SystemContent,
            MessageContent,
            PredictionContent,
            ToolDefinitions,
            ToolSelection,
        ],
    ) -> int:
        ...
