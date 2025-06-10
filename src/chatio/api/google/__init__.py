
from typing import override

from chatio.api._common import ApiConfig

from chatio.api._common import ChatApi


from .params import GoogleParams
from .format import GoogleFormat
from .client import GoogleClient


class GoogleApi(ChatApi):
    def __init__(self, config: ApiConfig):
        super().__init__(config)

        params = GoogleParams(**config.options if config.options else {})

        self._format = GoogleFormat(params)
        self._client = GoogleClient(config, params)

    @property
    @override
    def format(self):
        return self._format

    @property
    @override
    def client(self):
        return self._client
