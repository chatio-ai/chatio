
from collections.abc import Iterator

from typing import override


from google.genai import Client
from google.genai.types import HttpOptions


from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.events import ChatEvent

from chatio.api.helper.httpx import httpx_args


from .config import GoogleConfig
from .format import GoogleFormat
from .events import _pump


class GoogleClient(ApiClient):

    def __init__(self, config: GoogleConfig):
        self._client = Client(
            # base_url=config.api_url,
            api_key=config.api_key,
            http_options=HttpOptions(client_args=httpx_args()))

        self._format = GoogleFormat(config)

    # streams

    @override
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> Iterator[ChatEvent]:
        _params = self._format.build(state, tools)
        return _pump(lambda: self._client.models.generate_content_stream(
            model=model,
            config={
                'max_output_tokens': 4096,
                'tools': _params.tools,
                'system_instruction': _params.system,
                'tool_config': _params.tool_choice,
            },
            contents=_params.messages,
        ))

    # helpers

    @override
    def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        raise NotImplementedError
