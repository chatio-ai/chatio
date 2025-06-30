
from collections.abc import Iterator

from typing import override


from httpx import Client as HttpxClient

from openai import OpenAI


from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.events import ChatEvent


from chatio.api.helper.httpx import httpx_args


from .config import OpenAIConfigFormat
from .config import OpenAIConfigVendor
from .format import OpenAIFormat
from .events import _pump


class OpenAIClient(ApiClient):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = OpenAIConfigFormat(**config.get('options', {}))
        _config_vendor = OpenAIConfigVendor(**config.get('vendor', {}))

        self._format = OpenAIFormat(_config_format)

        self._client = OpenAI(
            api_key=_config_vendor.api_key,
            base_url=_config_vendor.base_url,
            http_client=HttpxClient(**httpx_args()))

    # streams

    @override
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> Iterator[ChatEvent]:
        params = self._format.format(state, tools)

        _messages = [*params.options.system, *params.messages]

        if params.options.prediction:
            return _pump(self._client.beta.chat.completions.stream(
                stream_options={'include_usage': True},
                model=model,
                messages=_messages,
                prediction=params.options.prediction,
            ))

        return _pump(self._client.beta.chat.completions.stream(
            max_completion_tokens=4096,
            stream_options={'include_usage': True},
            model=model,
            messages=_messages,
            prediction=params.options.prediction,
            tools=params.tools.tools,
            tool_choice=params.tools.tool_choice,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        raise NotImplementedError
