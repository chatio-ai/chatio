
from typing import override

from chatio.core import ApiHelper

from .config import ClaudeConfig
from .params import ClaudeParams
from .client import ClaudeClient


class ClaudeApi(ApiHelper[ClaudeParams]):

    def __init__(self, config: ClaudeConfig) -> None:
        self._config = config

        self._params = ClaudeParams(config)
        self._client = ClaudeClient(config)

    @property
    @override
    def config(self) -> ClaudeConfig:
        return self._config

    @property
    @override
    def params(self) -> ClaudeParams:
        return self._params

    @property
    @override
    def client(self) -> ClaudeClient:
        return self._client
