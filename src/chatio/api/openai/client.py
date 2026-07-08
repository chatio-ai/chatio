
from typing import override

from openai import AsyncOpenAI

from openai.resources import chat


from chatio.api.helper.httpx import httpx_client

from chatio.core.client import ApiClient


from .config import OpenAIClientConfig
from .params import OpenAIParams
from .stream import OpenAIStream


_chat = chat


class OpenAIClient(ApiClient[
    OpenAIParams,
]):

    def __init__(self, config: OpenAIClientConfig, client: AsyncOpenAI | None = None) -> None:
        if client is None:
            client = AsyncOpenAI(
                api_key=config.api_key,
                base_url=config.base_url,
                http_client=httpx_client())

        self._client = client

    # streams

    @override
    def iterate_model_events(self, model: str, params: OpenAIParams) -> OpenAIStream:
        messages = [*params.system, *params.messages]

        if params.prediction:
            return OpenAIStream(self._client.chat.completions.stream(
                stream_options={'include_usage': True},
                model=model,
                messages=messages,
                prediction=params.prediction,
            ))

        return OpenAIStream(self._client.chat.completions.stream(
            stream_options={'include_usage': True},
            model=model,
            messages=messages,
            prediction=params.prediction,
            tools=params.tools,
            tool_choice=params.tool_choice,
        ))

    # helpers

    @override
    async def count_message_tokens(self, model: str, params: OpenAIParams) -> int:
        raise NotImplementedError

    @override
    async def close(self) -> None:
        await self._client.close()
