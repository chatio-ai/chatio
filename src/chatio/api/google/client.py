
from typing import override

from google.genai import Client
from google.genai.types import HttpOptions


from chatio.api.helper.httpx import httpx_args

from chatio.core.client import ApiClient


from .config import GoogleConfigClient
from .params import GoogleParams
from .stream import GoogleStream


class GoogleClient(ApiClient[
    GoogleParams,
]):

    def __init__(self, config: GoogleConfigClient, client: Client | None = None) -> None:
        if client is None:
            client = Client(
                api_key=config.api_key,
                http_options=HttpOptions(
                    base_url=config.base_url,
                    async_client_args=httpx_args(),
                ))

        self._client = client.aio

    # streams

    @override
    def iterate_model_events(self, model: str, params: GoogleParams) -> GoogleStream:
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
    async def count_message_tokens(self, model: str, params: GoogleParams) -> int:
        raise NotImplementedError

    @override
    async def close(self) -> None:
        pass
