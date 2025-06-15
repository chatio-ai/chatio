
from typing import override

from chatio.api._common import ChatConfig

from chatio.api._common import ChatApi


from .params import ClaudeParams
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeApi(ChatApi):
    def __init__(self, config: ChatConfig):
        super().__init__()

        self._config = config

        params = ClaudeParams(**config.config.options if config.config.options else {})

        self._format = ClaudeFormat(params)
        self._client = ClaudeClient(config.config, params)

    @property
    @override
    def config(self):
        return self._config

    @property
    @override
    def format(self):
        return self._format

    @property
    @override
    def client(self):
        return self._client
