
from typing import override

from httpx import AsyncClient as HttpxClient

from openai import AsyncOpenAI


from chatio.api.helper.httpx import httpx_args

from chatio.core.client import ApiClient


from .compat import AsyncCompat


from .config import OpenAIConfigClient
from .params import OpenAIParams
from .stream import OpenAIStream


class OpenAIClient(ApiClient[
    OpenAIParams,
]):

    def __init__(self, config: OpenAIConfigClient) -> None:
        if not config.base_url:
            self._client = AsyncOpenAI(
                api_key=config.api_key,
                http_client=HttpxClient(**httpx_args()))
        else:
            self._client = AsyncCompat(
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
