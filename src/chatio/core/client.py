
from abc import ABC, abstractmethod

from typing import override

from .object import Closeable

from .config import ApiConfigFormat
from .models import ChatState
from .models import ChatTools
from .params import ApiParams
from .format import ApiFormat
from .stream import ApiStream


class ApiClient(Closeable, ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        ...

    @abstractmethod
    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        ...


class ApiClientImpl[
    ApiParamsT: ApiParams,
](Closeable, ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, params: ApiParamsT) -> ApiStream:
        ...

    @abstractmethod
    async def count_message_tokens(self, model: str, params: ApiParamsT) -> int:
        ...


class ApiClientBase[
    ApiConfigT: ApiConfigFormat,
    ApiParamsT: ApiParams,
](ApiClient, ABC):

    @property
    @abstractmethod
    def _format(self) -> ApiFormat[
        ApiConfigT,
        ApiParamsT,
    ]:
        ...

    @property
    @abstractmethod
    def _client(self) -> ApiClientImpl[ApiParamsT]:
        ...

    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        params = self._format.format(state, tools)
        return self._client.iterate_model_events(model, params)

    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        params = self._format.format(state, tools)
        return await self._client.count_message_tokens(model, params)

    @override
    async def close(self) -> None:
        await self._client.close()
