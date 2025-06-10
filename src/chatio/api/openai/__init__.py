
from typing import override

from chatio.api._common import ApiConfig

from chatio.api._common import ChatApi


from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIApi(ChatApi):
    def __init__(self, config: ApiConfig):
        super().__init__(config)

        params = OpenAIParams(**config.options if config.options else {})

        self._format = OpenAIFormat(params)
        self._client = OpenAIClient(config, params, self._format)

    @property
    @override
    def format(self):
        return self._format

    @property
    @override
    def client(self):
        return self._client
