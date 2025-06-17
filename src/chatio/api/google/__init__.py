
from typing import override

from google.genai.types import PartDict
from google.genai.types import ContentDict
from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionDeclarationDict


from chatio.core.config import ApiHelper
from chatio.core.config import ModelConfig


from .format import GoogleFormat
from .client import GoogleClient
from .config import GoogleConfig


class GoogleApi(ApiHelper[
    ContentDict,
    ContentDict,
    None,
    PartDict,
    PartDict,
    FunctionDeclarationDict,
    ToolListUnionDict,
    ToolConfigDict,
]):

    def __init__(self, model: ModelConfig, config: GoogleConfig):
        self._model = model

        # config = GoogleConfig(**config.config.api if config.config.api else {})

        self._format = GoogleFormat(config)
        self._client = GoogleClient(config)

    @property
    @override
    def config(self) -> ModelConfig:
        return self._model

    @property
    @override
    def format(self) -> GoogleFormat:
        return self._format

    @property
    @override
    def client(self) -> GoogleClient:
        return self._client
