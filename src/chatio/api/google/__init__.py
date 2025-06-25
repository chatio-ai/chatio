
from typing import override

from google.genai.types import PartDict
from google.genai.types import ContentDict
from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionDeclarationDict


from chatio.core import ApiIfaces


from .config import GoogleConfig
from .format import GoogleFormat
from .client import GoogleClient


class GoogleApi(ApiIfaces[
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

        self._format = GoogleFormat(config)
        self._client = GoogleClient(config)

    @property
    @override
    def config(self) -> GoogleConfig:
        return self._config

    @property
    @override
    def format(self) -> GoogleFormat:
        return self._format

    @property
    @override
    def client(self) -> GoogleClient:
        return self._client
