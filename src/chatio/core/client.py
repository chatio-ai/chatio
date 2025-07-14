
from abc import ABC, abstractmethod

from .object import Closeable

from .models import ChatState
from .models import ChatTools
from .stream import ApiStream


class ApiClient(Closeable, ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        ...

    @abstractmethod
    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        ...
