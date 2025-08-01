
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from anthropic import Anthropic


from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args

from .config import ClaudeConfigFormat
from .config import ClaudeConfigClient
from .format import ClaudeFormat
from .events import _pump


class ClaudeClient(ApiClient):

    @override
    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = ClaudeConfigFormat(**config.get('format', {}))
        _config_client = ClaudeConfigClient(**config.get('client', {}))

        self._format = ClaudeFormat(_config_format)

        self._client = Anthropic(
            api_key=_config_client.api_key,
            base_url=_config_client.base_url,
            http_client=HttpxClient(**httpx_args()))

    # streams

    @override
    def iterate_model_events(
            self, model: str, state: ChatState, tools: ChatTools) -> Iterator[ChatEvent]:

        params = self._format.format(state, tools)

        return _pump(self._client.messages.stream(
            max_tokens=4096,
            model=model,
            system=params.options.system,
            messages=params.messages,
            tools=params.tools.tools,
            tool_choice=params.tools.tool_choice,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        params = self._format.format(state, tools)

        result = self._client.messages.count_tokens(
            model=model,
            system=params.options.system,
            messages=params.messages,
            tools=params.tools.tools,
            tool_choice=params.tools.tool_choice,
        )

        return result.input_tokens

    @override
    def close(self) -> None:
        self._client.close()
