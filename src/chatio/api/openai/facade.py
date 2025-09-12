
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import OpenAIConfigFormat
from .config import OpenAIConfigClient
from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIFacadeDeps(ApiFacadeDeps[
    OpenAIConfigFormat,
    OpenAIParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:
        self._config = config

    @property
    @override
    def format(self) -> OpenAIFormat:
        _config_format = OpenAIConfigFormat(**self._config.get('format', {}))
        return OpenAIFormat(_config_format)

    @property
    @override
    def client(self) -> OpenAIClient:
        _config_client = OpenAIConfigClient(**self._config.get('client', {}))
        return OpenAIClient(_config_client)
