
from typing import override

from google.genai import Client
from google.genai.types import HttpOptions

from google.genai.types import ContentUnionDict

from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiParams

from chatio.core.client import ApiClientImpl

from chatio.api.helper.httpx import httpx_args


from .config import GoogleConfigFormat
from .config import GoogleConfigClient
from .params import GoogleStateOptions
from .format import GoogleFormat
from .stream import GoogleStream


class GoogleClient(ApiClientImpl[
    ContentUnionDict,
    GoogleStateOptions,
    ToolListUnionDict | None,
    ToolConfigDict | None,
]):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_client = GoogleConfigClient(**config.get('client', {}))
        _config_format = GoogleConfigFormat(**config.get('format', {}))

        self._formatter = GoogleFormat(_config_format)

        self._client = Client(
            api_key=_config_client.api_key,
            http_options=HttpOptions(
                base_url=_config_client.base_url,
                async_client_args=httpx_args(),
            )).aio

    # formats

    @override
    def _format(self, state: ChatState, tools: ChatTools) -> ApiParams[
        ContentUnionDict,
        GoogleStateOptions,
        ToolListUnionDict | None,
        ToolConfigDict | None,
    ]:
        return self._formatter.format(state, tools)

    # streams

    @override
    def _iterate_model_events(self, model: str, params: ApiParams[
        ContentUnionDict,
        GoogleStateOptions,
        ToolListUnionDict | None,
        ToolConfigDict | None,
    ]) -> GoogleStream:
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
    async def _count_message_tokens(self, model: str, params: ApiParams[
        ContentUnionDict,
        GoogleStateOptions,
        ToolListUnionDict | None,
        ToolConfigDict | None,
    ]) -> int:
        raise NotImplementedError

    @override
    async def close(self) -> None:
        pass
