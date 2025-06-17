
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from openai import OpenAI
from openai import NOT_GIVEN

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.client import ChatClient
from chatio.core.kwargs import ChatKwargs
from chatio.core.events import ChatEvent

from chatio.core.config import ApiConfig

from chatio.api.helper.httpx import httpx_args


from .params import OpenAIParams
from .format import OpenAIFormat

from .events import _pump


class OpenAIClient(ChatClient[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    def __init__(self, config: ApiConfig, params: OpenAIParams, format_: OpenAIFormat):
        self._client = OpenAI(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = params
        self._format = format_

    # events

    @override
    def iterate_model_events(
        self, model: str,
        state: ChatKwargs[
            ChatCompletionMessageParam,
            ChatCompletionMessageParam,
            ChatCompletionPredictionContentParam,
            list[ChatCompletionToolParam],
            ChatCompletionToolChoiceOptionParam,
        ],
    ) -> Iterator[ChatEvent]:
        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            max_completion_tokens=4096 if state.prediction is None else NOT_GIVEN,
            stream_options={'include_usage': True},
            tools=state.tools if state.tools is not None and state.prediction is None else NOT_GIVEN,
            messages=[state.system, *state.messages] if state.system is not None else state.messages,
            tool_choice=state.tool_choice if state.tool_choice is not None else NOT_GIVEN,
            prediction=state.prediction if state.prediction is not None else NOT_GIVEN,
        ))

    @override
    def count_message_tokens(
        self, model: str,
        state: ChatKwargs[
            ChatCompletionMessageParam,
            ChatCompletionMessageParam,
            ChatCompletionPredictionContentParam,
            list[ChatCompletionToolParam],
            ChatCompletionToolChoiceOptionParam,
        ],
    ) -> int:
        raise NotImplementedError
