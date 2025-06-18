
from typing import override

from google.genai.types import PartDict
from google.genai.types import ContentDict
from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionDeclarationDict


from chatio.core import ApiHelper


from .config import GoogleConfig
from .params import GoogleParams
from .format import GoogleFormat
from .client import GoogleClient


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

    def __init__(self, config: GoogleConfig) -> None:
        self._config = config

        self._params = GoogleParams()
        self._format = GoogleFormat(config)
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
    def format(self) -> GoogleFormat:
        return self._format

    @property
    @override
    def client(self) -> GoogleClient:
        return self._client
