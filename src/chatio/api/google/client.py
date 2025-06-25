
from collections.abc import Iterator

from typing import override


from google.genai import Client
from google.genai.types import HttpOptions

from google.genai.types import ContentDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.client import ApiClient
from chatio.core.config import ApiConfig
from chatio.core.params import ApiParams

from chatio.core.events import ChatEvent

from chatio.api.helper.httpx import httpx_args


from .events import _pump


class GoogleClient(ApiClient[
    ContentDict,
    ContentDict,
    None,
    ToolListUnionDict,
    ToolConfigDict,
]):

    def __init__(self, config: ApiConfig):
        self._client = Client(
            # base_url=config.api_url,
            api_key=config.api_key,
            http_options=HttpOptions(client_args=httpx_args()))

    # streams

    @override
    def iterate_model_events(
        self, model: str,
        params: ApiParams[
            ContentDict,
            ContentDict,
            None,
            ToolListUnionDict,
            ToolConfigDict,
        ],
    ) -> Iterator[ChatEvent]:
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
    def count_message_tokens(
        self, model: str,
        params: ApiParams[
            ContentDict,
            ContentDict,
            None,
            ToolListUnionDict,
            ToolConfigDict,
        ],
    ) -> int:
        raise NotImplementedError
