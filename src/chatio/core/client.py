
from abc import ABC, abstractmethod

from typing import Protocol

from .object import SupportsCloseable
from .object import Closeable

from .config import ApiConfigFormat
from .models import ChatState
from .models import ChatTools
from .params import ApiParams
from .format import ApiFormat
from .stream import ApiStream


class ApiClientImpl[
    ApiConfigT: ApiConfigFormat,
    ApiParamsT: ApiParams,
](Closeable, ABC):

    @property
    @abstractmethod
    def _format(self) -> ApiFormat[
        ApiConfigT,
        ApiParamsT,
    ]:
        ...

    @abstractmethod
    def _iterate_model_events(self, model: str, params: ApiParamsT) -> ApiStream:
        ...

    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        params = self._format.format(state, tools)
        return self._iterate_model_events(model, params)

    @abstractmethod
    async def _count_message_tokens(self, model: str, params: ApiParamsT) -> int:
        ...

    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        params = self._format.format(state, tools)
        return await self._count_message_tokens(model, params)


class ApiClient(SupportsCloseable, Protocol):

    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        ...

    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        ...
