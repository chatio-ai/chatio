
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from openai import OpenAI
from openai import NOT_GIVEN


from chatio.core.client import ApiClient
from chatio.core.config import ApiConfig

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args


from .params import OpenAIParams
from .events import _pump


class OpenAIClient(ApiClient[OpenAIParams]):

    def __init__(self, config: ApiConfig):
        self._client = OpenAI(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

    # streams

    @override
    def iterate_model_events(self, model: str, params: OpenAIParams) -> Iterator[ChatEvent]:
        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            max_completion_tokens=4096 if params.prediction is None else NOT_GIVEN,
            stream_options={'include_usage': True},
            tools=params.tools if params.tools is not None and params.prediction is None else NOT_GIVEN,
            messages=[params.system, *params.messages] if params.system is not None else params.messages,
            tool_choice=params.tool_choice if params.tool_choice is not None else NOT_GIVEN,
            prediction=params.prediction if params.prediction is not None else NOT_GIVEN,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, params: OpenAIParams) -> int:
        raise NotImplementedError
