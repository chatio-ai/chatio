
from typing import override

from httpx import AsyncClient as HttpxClient

from anthropic import AsyncAnthropic


from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.client import ApiClientImpl

from chatio.api.helper.httpx import httpx_args


from .config import ClaudeConfigFormat
from .config import ClaudeConfigClient
from .params import ClaudeParams
from .format import ClaudeFormat
from .stream import ClaudeStream


class ClaudeClient(ApiClientImpl[ClaudeParams]):

    @override
    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = ClaudeConfigFormat(**config.get('format', {}))
        _config_client = ClaudeConfigClient(**config.get('client', {}))

        self._formatter = ClaudeFormat(_config_format)

        self._client = AsyncAnthropic(
            api_key=_config_client.api_key,
            base_url=_config_client.base_url,
            http_client=HttpxClient(**httpx_args()))

    # formats

    @override
    def _format(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        return self._formatter.format(state, tools)

    # streams

    @override
    def _iterate_model_events(self, model: str, params: ClaudeParams) -> ClaudeStream:
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
    async def _count_message_tokens(self, model: str, params: ClaudeParams) -> int:
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
