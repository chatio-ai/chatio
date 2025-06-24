
from typing import override

from chatio.core import ApiHelper

from .config import OpenAIConfig
from .params import OpenAIParams
from .client import OpenAIClient


class OpenAIApi(ApiHelper[OpenAIParams]):

    def __init__(self, config: OpenAIConfig) -> None:
        self._config = config

        self._params = OpenAIParams(config)
        self._client = OpenAIClient(config)

    @property
    @override
    def config(self) -> OpenAIConfig:
        return self._config

    @property
    @override
    def params(self) -> OpenAIParams:
        return self._params

    @property
    @override
    def client(self) -> OpenAIClient:
        return self._client
