
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from openai import OpenAI
from openai import NOT_GIVEN

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionToolParam


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
    list[ChatCompletionToolParam],
]):

    def __init__(self, config: ApiConfig, params: OpenAIParams, format_: OpenAIFormat):
        self._client = OpenAI(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = params
        self._format = format_

    # events

    def _iterate_model_events_prediction(self, model, _system, messages, prediction) -> Iterator[ChatEvent]:
        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            stream_options={'include_usage': True},
            messages=messages,
            prediction=prediction))

    @override
    def iterate_model_events(
        self, model: str,
        state: ChatKwargs[
            ChatCompletionMessageParam,
            ChatCompletionMessageParam,
            list[ChatCompletionToolParam],
        ],
    ) -> Iterator[ChatEvent]:
        # prediction = kwargs.pop('prediction', None)
        # if self._params.prediction and prediction:
        #     prediction = self._format.predict_content(prediction)
        #     return self._iterate_model_events_prediction(model, system, messages, prediction)

        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            max_completion_tokens=4096,
            stream_options={'include_usage': True},
            tools=state.tools if state.tools is not None else NOT_GIVEN,
            messages=[state.system, *state.messages] if state.system is not None else state.messages,
        ))

    @override
    def count_message_tokens(
        self, model: str,
        state: ChatKwargs[
            ChatCompletionMessageParam,
            ChatCompletionMessageParam,
            list[ChatCompletionToolParam],
        ],
    ) -> int:
        raise NotImplementedError
