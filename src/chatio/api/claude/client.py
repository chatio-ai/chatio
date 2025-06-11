
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from anthropic import Anthropic

from anthropic.types import MessageParam
from anthropic.types import TextBlockParam


from chatio.core.events import ChatEvent
from chatio.core.client import ChatClient

from chatio.core.config import ApiConfig

from chatio.api.helper.httpx import httpx_args


from .params import ClaudeParams

from .events import _pump


class ClaudeClient(ChatClient[TextBlockParam, MessageParam]):

    @override
    def __init__(self, config: ApiConfig, params: ClaudeParams) -> None:
        self._client = Anthropic(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = params

    # events

    @override
    def iterate_model_events(self, model, system: TextBlockParam | None,
                             messages: list[MessageParam], tools) -> Iterator[ChatEvent]:
        system_ = [system] if system is not None else []

        return _pump(self._client.messages.stream(
            model=model,
            max_tokens=4096,
            tools=tools,
            system=system_,
            messages=messages))

    # helpers

    @override
    def count_message_tokens(self, model, system: TextBlockParam | None,
                             messages: list[MessageParam], tools) -> int:
        system_ = [system] if system is not None else []

        return self._client.messages.count_tokens(
            model=model,
            tools=tools,
            system=system_,
            messages=messages).input_tokens
