
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from anthropic import Anthropic
from anthropic import NOT_GIVEN

from chatio.core.mapper import ApiMapper
from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args


from .config import ClaudeConfig
from .format import ClaudeFormat
# from .params import ClaudeParams
from .events import _pump


class ClaudeClient(ApiClient):

    @override
    def __init__(self, config: ClaudeConfig) -> None:
        self._client = Anthropic(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._mapper = ApiMapper(ClaudeFormat(config))

    # streams

    @override
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> Iterator[ChatEvent]:
        _params = self._mapper(state, tools)
        return _pump(self._client.messages.stream(
            model=model,
            max_tokens=4096,
            tools=_params.tools if _params.tools is not None else NOT_GIVEN,
            system=[_params.system] if _params.system is not None else NOT_GIVEN,
            messages=_params.messages,
            tool_choice=_params.tool_choice if _params.tool_choice is not None else NOT_GIVEN,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        _params = self._mapper(state, tools)
        return self._client.messages.count_tokens(
            model=model,
            tools=_params.tools if _params.tools is not None else NOT_GIVEN,
            system=[_params.system] if _params.system is not None else NOT_GIVEN,
            messages=_params.messages,
            tool_choice=_params.tool_choice if _params.tool_choice is not None else NOT_GIVEN,
        ).input_tokens
