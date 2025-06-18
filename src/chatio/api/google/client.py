
from collections.abc import Iterator

from typing import override


from google.genai import Client
from google.genai.types import HttpOptions


from chatio.core.client import ApiClient
from chatio.core.config import ApiConfig

from chatio.core.events import ChatEvent

from chatio.api.helper.httpx import httpx_args


from .params import GoogleParams
from .events import _pump


class GoogleClient(ApiClient[GoogleParams]):

    def __init__(self, config: ApiConfig):
        self._client = Client(
            # base_url=config.api_url,
            api_key=config.api_key,
            http_options=HttpOptions(client_args=httpx_args()))

    # streams

    @override
    def iterate_model_events(self, model: str, params: GoogleParams) -> Iterator[ChatEvent]:
        return _pump(lambda: self._client.models.generate_content_stream(
            model=model,
            config={
                'max_output_tokens': 4096,
                'tools': params.tools,
                'system_instruction': params.system,
                'tool_config': params.tool_choice,
            },
            contents=params.messages,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, params: GoogleParams) -> int:
        raise NotImplementedError
