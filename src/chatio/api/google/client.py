
from collections.abc import Iterator

from typing import override


from google.genai.types import HttpOptions
from google.genai import Client


from chatio.core.events import ChatEvent

from chatio.api._common import ChatClient
from chatio.api._common import ApiConfig

from chatio.api._utils import httpx_args


from .params import GoogleParams

from .events import _pump


class GoogleClient(ChatClient):

    def __init__(self, config: ApiConfig, params: GoogleParams):
        self._client = Client(
            # base_url=config.api_url,
            api_key=config.api_key,
            http_options=HttpOptions(client_args=httpx_args()))

        self._params = params

    @override
    def iterate_model_events(self, model, system, messages, tools, **_kwargs) -> Iterator[ChatEvent]:
        return _pump(lambda: self._client.models.generate_content_stream(
            model=model,
            config={
                'max_output_tokens': 4096,
                'tools': tools,
                'system_instruction': system,
            },
            contents=messages))

    @override
    def count_message_tokens(self, model, system, messages, tools):
        raise NotImplementedError
