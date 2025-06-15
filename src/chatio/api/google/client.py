
from collections.abc import Iterator

from typing import override


from google.genai import Client
from google.genai.types import HttpOptions

from google.genai.types import ContentDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.client import ChatClient
from chatio.core.kwargs import ChatKwargs
from chatio.core.events import ChatEvent

from chatio.core.config import ApiConfig

from chatio.api.helper.httpx import httpx_args


from .params import GoogleParams

from .events import _pump


class GoogleClient(ChatClient[
    ContentDict,
    ContentDict,
    ToolListUnionDict,
    ToolConfigDict,
]):

    def __init__(self, config: ApiConfig, params: GoogleParams):
        self._client = Client(
            # base_url=config.api_url,
            api_key=config.api_key,
            http_options=HttpOptions(client_args=httpx_args()))

        self._params = params

    @override
    def iterate_model_events(
        self, model: str,
        state: ChatKwargs[
            ContentDict,
            ContentDict,
            ToolListUnionDict,
            ToolConfigDict,
        ],
    ) -> Iterator[ChatEvent]:
        return _pump(lambda: self._client.models.generate_content_stream(
            model=model,
            config={
                'max_output_tokens': 4096,
                'tools': state.tools,
                'system_instruction': state.system,
                'tool_config': state.tool_choice,
            },
            contents=state.messages,
        ))

    @override
    def count_message_tokens(
        self, model: str,
        state: ChatKwargs[
            ContentDict,
            ContentDict,
            ToolListUnionDict,
            ToolConfigDict,
        ],
    ) -> int:
        raise NotImplementedError
