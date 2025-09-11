
from abc import ABC, abstractmethod

from typing import Protocol

from .object import SupportsCloseable
from .object import Closeable

from .models import ChatState
from .models import ChatTools
from .params import ApiParams
from .params import ApiStateOptions
from .stream import ApiStream


class ApiClientImpl[
    ChatMessageT,
    ApiStateOptionsT: ApiStateOptions,
    ToolDefinitionsT,
    ToolChoiceT,
](Closeable, ABC):

    @abstractmethod
    def _format(self, state: ChatState, tools: ChatTools) -> ApiParams[
        ChatMessageT,
        ApiStateOptionsT,
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        ...

    @abstractmethod
    def _iterate_model_events(self, model: str, params: ApiParams[
        ChatMessageT,
        ApiStateOptionsT,
        ToolDefinitionsT,
        ToolChoiceT,
    ]) -> ApiStream:
        ...

    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        params = self._format(state, tools)
        return self._iterate_model_events(model, params)

    @abstractmethod
    async def _count_message_tokens(self, model: str, params: ApiParams[
        ChatMessageT,
        ApiStateOptionsT,
        ToolDefinitionsT,
        ToolChoiceT,
    ]) -> int:
        ...

    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        params = self._format(state, tools)
        return await self._count_message_tokens(model, params)


class ApiClient(SupportsCloseable, Protocol):

    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        ...

    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        ...
