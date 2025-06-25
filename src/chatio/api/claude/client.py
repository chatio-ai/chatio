
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from anthropic import Anthropic
from anthropic import NOT_GIVEN

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam


from chatio.core.client import ApiClient
from chatio.core.config import ApiConfig
from chatio.core.params import ApiParams

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args


from .events import _pump


class ClaudeClient(ApiClient[
    TextBlockParam,
    MessageParam,
    None,
    list[ToolParam],
    ToolChoiceParam,
]):

    @override
    def __init__(self, config: ApiConfig) -> None:
        self._client = Anthropic(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

    # streams

    @override
    def iterate_model_events(
        self, model: str,
        params: ApiParams[
            TextBlockParam,
            MessageParam,
            None,
            list[ToolParam],
            ToolChoiceParam,
        ],
    ) -> Iterator[ChatEvent]:

        return _pump(self._client.messages.stream(
            model=model,
            max_tokens=4096,
            tools=params.tools if params.tools is not None else NOT_GIVEN,
            system=[params.system] if params.system is not None else NOT_GIVEN,
            messages=params.messages,
            tool_choice=params.tool_choice if params.tool_choice is not None else NOT_GIVEN,
        ))

    # helpers

    @override
    def count_message_tokens(
        self, model: str,
        params: ApiParams[
            TextBlockParam,
            MessageParam,
            None,
            list[ToolParam],
            ToolChoiceParam,
        ],
    ) -> int:

        return self._client.messages.count_tokens(
            model=model,
            tools=params.tools if params.tools is not None else NOT_GIVEN,
            system=[params.system] if params.system is not None else NOT_GIVEN,
            messages=params.messages,
            tool_choice=params.tool_choice if params.tool_choice is not None else NOT_GIVEN,
        ).input_tokens
