
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from openai import OpenAI
from openai import NOT_GIVEN


from chatio.core.client import ApiClient
from chatio.core.params import ApiParams

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args


from .config import OpenAIConfig
from .format import OpenAIFormat
from .params import OpenAIParams
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
    def iterate_model_events(self, model: str, params: ApiParams) -> Iterator[ChatEvent]:
        _params = OpenAIParams(params, self._format)
        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            max_completion_tokens=4096 if _params.prediction is None else NOT_GIVEN,
            stream_options={'include_usage': True},
            tools=_params.tools if _params.tools is not None and _params.prediction is None else NOT_GIVEN,
            messages=[_params.system, *_params.messages] if _params.system is not None else _params.messages,
            tool_choice=_params.tool_choice if _params.tool_choice is not None else NOT_GIVEN,
            prediction=_params.prediction if _params.prediction is not None else NOT_GIVEN,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, params: ApiParams) -> int:
        raise NotImplementedError
