
from typing import override

from google.genai import Client
from google.genai.types import HttpOptions


from chatio.core.client import ApiClient

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.api.helper.httpx import httpx_args


from .config import GoogleConfigFormat
from .config import GoogleConfigClient
from .format import GoogleFormat
from .stream import GoogleStream


class GoogleClient(ApiClient):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_client = GoogleConfigClient(**config.get('client', {}))
        _config_format = GoogleConfigFormat(**config.get('format', {}))

        self._format = GoogleFormat(_config_format)

        self._client = Client(
            api_key=_config_client.api_key,
            http_options=HttpOptions(
                base_url=_config_client.base_url,
                client_args=httpx_args(),
            )).aio

    # streams

    @override
    def iterate_model_events(self, model: str, state: ChatState, tools: ChatTools) -> GoogleStream:
        params = self._format.format(state, tools)

        return GoogleStream(lambda: self._client.models.generate_content_stream(
            model=model,
            config={
                'tools': params.tools.tools,
                'tool_config': params.tools.tool_choice,
                'system_instruction': params.options.system,
            },
            contents=params.messages,
        ))

    # helpers

    @override
    async def count_message_tokens(self, model: str, state: ChatState, tools: ChatTools) -> int:
        raise NotImplementedError

    @override
    async def close(self) -> None:
        pass
