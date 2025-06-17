
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from anthropic import Anthropic
from anthropic import NOT_GIVEN

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam


from chatio.core.client import ChatClient
from chatio.core.kwargs import ChatKwargs
from chatio.core.events import ChatEvent

from chatio.core.config import ApiConfig

from chatio.api.helper.httpx import httpx_args


from .params import ClaudeParams

from .events import _pump


class ClaudeClient(ChatClient[
    TextBlockParam,
    MessageParam,
    None,
    list[ToolParam],
    ToolChoiceParam,
]):

    @override
    def __init__(self, config: ApiConfig, params: ClaudeParams) -> None:
        self._client = Anthropic(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = params

    # events

    @override
    def iterate_model_events(
        self, model: str,
        state: ChatKwargs[
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
            tools=state.tools if state.tools is not None else NOT_GIVEN,
            system=[state.system] if state.system is not None else NOT_GIVEN,
            messages=state.messages,
            tool_choice=state.tool_choice if state.tool_choice is not None else NOT_GIVEN,
        ))

    # helpers

    @override
    def count_message_tokens(
        self, model: str,
        state: ChatKwargs[
            TextBlockParam,
            MessageParam,
            None,
            list[ToolParam],
            ToolChoiceParam,
        ],
    ) -> int:

        return self._client.messages.count_tokens(
            model=model,
            tools=state.tools if state.tools is not None else NOT_GIVEN,
            system=[state.system] if state.system is not None else NOT_GIVEN,
            messages=state.messages,
            tool_choice=state.tool_choice if state.tool_choice is not None else NOT_GIVEN,
        ).input_tokens
