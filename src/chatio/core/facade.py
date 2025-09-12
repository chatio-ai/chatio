
from abc import ABC, abstractmethod

from typing import override

from .object import Closeable

from .config import ApiConfigFormat
from .models import ChatState
from .models import ChatTools
from .params import ApiParams
from .format import ApiFormat
from .stream import ApiStream
from .client import ApiClient


class ApiFacadeDeps[
    ApiConfigT: ApiConfigFormat,
    ApiParamsT: ApiParams,
](ABC):

    def __init__(self, config: dict[str, dict]) -> None:
        self._config_format = config.get('format', {})
        self._config_client = config.get('client', {})

    @property
    @abstractmethod
    def format(self) -> ApiFormat[
        ApiConfigT,
        ApiParamsT,
    ]:
        ...

    @property
    @abstractmethod
    def client(self) -> ApiClient[
        ApiParamsT,
    ]:
        ...


class ApiFacade[
    ApiFacadeDepsT: ApiFacadeDeps,
](Closeable):

    def __init__(self, deps: ApiFacadeDepsT) -> None:
        self._format = deps.format
        self._client = deps.client

    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> ApiStream:
        params = self._format.format(state, tools)
        return self._client.iterate_model_events(model, params)

    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        params = self._format.format(state, tools)
        return await self._client.count_message_tokens(model, params)

    @override
    async def close(self) -> None:
        await self._client.close()
