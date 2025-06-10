
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from anthropic import Anthropic


from chatio.core.events import ChatEvent

from chatio.api._common import ChatClient
from chatio.api._common import ApiConfig

from chatio.api._utils import httpx_args


from .params import ClaudeParams

from .events import _pump


class ClaudeClient(ChatClient):

    @override
    def __init__(self, config: ApiConfig, params: ClaudeParams):
        self._client = Anthropic(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = params

    # events

    @override
    def iterate_model_events(self, model, system, messages, tools, **_kwargs) -> Iterator[ChatEvent]:
        return _pump(self._client.messages.stream(
            model=model,
            max_tokens=4096,
            tools=tools,
            system=system,
            messages=messages))

    # helpers

    @override
    def count_message_tokens(self, model, system, messages, tools):
        return self._client.messages.count_tokens(
            model=model,
            tools=tools,
            system=system,
            messages=messages).input_tokens
