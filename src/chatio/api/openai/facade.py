
from typing import override

from chatio.core.facade import ApiFacadeBase


from .config import OpenAIConfigFormat
from .config import OpenAIConfigClient
from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIFacade(ApiFacadeBase[
    OpenAIConfigFormat,
    OpenAIParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = OpenAIConfigFormat(**config.get('format', {}))
        _config_client = OpenAIConfigClient(**config.get('client', {}))

        self._formatter = OpenAIFormat(_config_format)
        self._client_do = OpenAIClient(_config_client)

    @property
    @override
    def _format(self) -> OpenAIFormat:
        return self._formatter

    @property
    @override
    def _client(self) -> OpenAIClient:
        return self._client_do
