
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from openai import OpenAI


from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args


from .config import OpenAIConfig
from .format import OpenAIFormat
from .events import _pump


class OpenAIClient(ApiClient):

    def __init__(self, config: OpenAIConfig):
        self._client = OpenAI(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._format = OpenAIFormat(config)

    # streams

    @override
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> Iterator[ChatEvent]:
        _params = self._format.build(state, tools)

        return _pump(self._client.beta.chat.completions.stream(
            max_completion_tokens=_params.max_completion_tokens,
            stream_options={'include_usage': True},
            model=model,
            messages=_params.messages,
            prediction=_params.prediction,
            tools=_params.tools,
            tool_choice=_params.tool_choice,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        raise NotImplementedError
