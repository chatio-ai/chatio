
from typing import override

from chatio.api._common import ChatConfig

from chatio.api._common import ChatApi


from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIApi(ChatApi):
    def __init__(self, config: ChatConfig):
        super().__init__()

        self._config = config

        params = OpenAIParams(**config.config.options if config.config.options else {})

        self._format = OpenAIFormat(params)
        self._client = OpenAIClient(config.config, params, self._format)

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
