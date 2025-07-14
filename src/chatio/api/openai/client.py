
from typing import override

from httpx import AsyncClient as HttpxClient

from openai import AsyncOpenAI


from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools


from chatio.api.helper.httpx import httpx_args


from .config import OpenAIConfigFormat
from .config import OpenAIConfigClient
from .format import OpenAIFormat
from .stream import OpenAIStream


class OpenAIClient(ApiClient):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = OpenAIConfigFormat(**config.get('format', {}))
        _config_client = OpenAIConfigClient(**config.get('client', {}))

        self._format = OpenAIFormat(_config_format)

        self._client = AsyncOpenAI(
            api_key=_config_client.api_key,
            base_url=_config_client.base_url,
            http_client=HttpxClient(**httpx_args()))

    # streams

    @override
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> OpenAIStream:
        params = self._format.format(state, tools)

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
    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        raise NotImplementedError

    @override
    async def close(self) -> None:
        await self._client.close()
