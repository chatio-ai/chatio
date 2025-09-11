
from typing import override

from httpx import AsyncClient as HttpxClient

from openai import AsyncOpenAI


from chatio.core.client import ApiClientImpl
from chatio.core.client import ApiClientBase

from chatio.api.helper.httpx import httpx_args


from .config import OpenAIConfigFormat
from .config import OpenAIConfigClient
from .params import OpenAIParams
from .format import OpenAIFormat
from .stream import OpenAIStream


class OpenAIClientImpl(ApiClientImpl[
    OpenAIParams,
]):

    def __init__(self, config: OpenAIConfigClient) -> None:
        self._client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            http_client=HttpxClient(**httpx_args()))

    # streams

    @override
    def iterate_model_events(self, model: str, params: OpenAIParams) -> OpenAIStream:
        _messages = [*params.options.system, *params.messages]

        if params.options.prediction:
            return OpenAIStream(self._client.chat.completions.stream(
                stream_options={'include_usage': True},
                model=model,
                messages=_messages,
                prediction=params.options.prediction,
            ))

        return OpenAIStream(self._client.chat.completions.stream(
            stream_options={'include_usage': True},
            model=model,
            messages=_messages,
            prediction=params.options.prediction,
            tools=params.tools.tools,
            tool_choice=params.tools.tool_choice,
        ))

    # helpers

    @override
    async def count_message_tokens(self, model: str, params: OpenAIParams) -> int:
        raise NotImplementedError

    @override
    async def close(self) -> None:
        await self._client.close()


class OpenAIClient(ApiClientBase[
    OpenAIConfigFormat,
    OpenAIParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = OpenAIConfigFormat(**config.get('format', {}))
        _config_client = OpenAIConfigClient(**config.get('client', {}))

        self._formatter = OpenAIFormat(_config_format)
        self._client_do = OpenAIClientImpl(_config_client)

    @property
    @override
    def _format(self) -> OpenAIFormat:
        return self._formatter

    @property
    @override
    def _client(self) -> OpenAIClientImpl:
        return self._client_do
