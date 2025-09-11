
from typing import override

from google.genai import Client
from google.genai.types import HttpOptions


from chatio.core.client import ApiClientImpl
from chatio.core.client import ApiClientBase

from chatio.api.helper.httpx import httpx_args


from .config import GoogleConfigFormat
from .config import GoogleConfigClient
from .params import GoogleParams
from .format import GoogleFormat
from .stream import GoogleStream


class GoogleClientImpl(ApiClientImpl[
    GoogleParams,
]):

    def __init__(self, config: GoogleConfigClient) -> None:
        self._client = Client(
            api_key=config.api_key,
            http_options=HttpOptions(
                base_url=config.base_url,
                async_client_args=httpx_args(),
            )).aio

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


class GoogleClient(ApiClientBase[
    GoogleConfigFormat,
    GoogleParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_client = GoogleConfigClient(**config.get('client', {}))
        _config_format = GoogleConfigFormat(**config.get('format', {}))

        self._formatter = GoogleFormat(_config_format)
        self._client_do = GoogleClientImpl(_config_client)

    @property
    @override
    def _format(self) -> GoogleFormat:
        return self._formatter

    @property
    @override
    def _client(self) -> GoogleClientImpl:
        return self._client_do
