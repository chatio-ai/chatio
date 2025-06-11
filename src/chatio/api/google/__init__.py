
from typing import override

from google.genai.types import PartDict
from google.genai.types import ContentDict


from chatio.core.config import ChatConfig
from chatio.core.config import ChatApi


from .params import GoogleParams
from .format import GoogleFormat
from .client import GoogleClient


class GoogleApi(ChatApi[ContentDict, ContentDict, PartDict, PartDict]):
    def __init__(self, config: ChatConfig):
        super().__init__()

        self._config = config

        params = GoogleParams(**config.config.options if config.config.options else {})

        self._format = GoogleFormat(params)
        self._client = GoogleClient(config.config, params)

    @property
    @override
    def config(self) -> ChatConfig:
        return self._config

    @property
    @override
    def format(self) -> GoogleFormat:
        return self._format

    @property
    @override
    def client(self) -> GoogleClient:
        return self._client
