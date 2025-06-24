
from typing import override

from chatio.core import ApiHelper

from .config import GoogleConfig
from .params import GoogleParams
from .client import GoogleClient


class GoogleApi(ApiHelper[GoogleParams]):

    def __init__(self, config: GoogleConfig) -> None:
        self._config = config

        self._params = GoogleParams(config)
        self._client = GoogleClient(config)

    @property
    @override
    def config(self) -> GoogleConfig:
        return self._config

    @property
    @override
    def params(self) -> GoogleParams:
        return self._params

    @property
    @override
    def client(self) -> GoogleClient:
        return self._client
