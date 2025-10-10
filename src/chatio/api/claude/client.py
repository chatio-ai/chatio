
from typing import override

from httpx import AsyncClient as HttpxClient

from anthropic import AsyncAnthropic


from chatio.api.helper.httpx import httpx_args

from chatio.core.client import ApiClient


from .config import ClaudeConfigClient
from .params import ClaudeParams
from .stream import ClaudeStream


class ClaudeClient(ApiClient[
    ClaudeParams,
]):

    def __init__(self, config: ClaudeConfigClient, client: AsyncAnthropic | None = None) -> None:
        if client is None:
            client = AsyncAnthropic(
                api_key=config.api_key,
                base_url=config.base_url,
                http_client=HttpxClient(**httpx_args()))

        self._client = client

    # streams

    @override
    def iterate_model_events(self, model: str, params: ClaudeParams) -> ClaudeStream:
        return ClaudeStream(self._client.messages.stream(
            max_tokens=4096,
            model=model,
            system=params.options.system,
            messages=params.messages,
            tools=params.tools.tools,
            tool_choice=params.tools.tool_choice,
        ))

    # helpers

    @override
    async def count_message_tokens(self, model: str, params: ClaudeParams) -> int:
        result = await self._client.messages.count_tokens(
            model=model,
            system=params.options.system,
            messages=params.messages,
            tools=params.tools.tools,
            tool_choice=params.tools.tool_choice,
        )

        return result.input_tokens

    @override
    async def close(self) -> None:
        await self._client.close()
