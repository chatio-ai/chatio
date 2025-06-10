
from typing import override

from chatio.api._common import ApiConfig

from chatio.api._common import ChatApi


from .params import ClaudeParams
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeApi(ChatApi):
    def __init__(self, config: ApiConfig):
        super().__init__(config)

        params = ClaudeParams(**config.options if config.options else {})

        self._format = ClaudeFormat(params)
        self._client = ClaudeClient(config, params)

    @property
    @override
    def format(self):
        return self._format

    @property
    @override
    def client(self):
        return self._client
