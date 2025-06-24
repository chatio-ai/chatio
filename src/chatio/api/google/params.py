
from dataclasses import dataclass

from typing import override

from google.genai.types import ContentDict
from google.genai.types import PartDict

from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionDeclarationDict


from chatio.core.params import ApiParams


from .config import GoogleConfig
from .format import GoogleFormat


@dataclass(init=False)
class GoogleParams(ApiParams[
    ContentDict,
    ContentDict,
    None,
    PartDict,
    PartDict,
    FunctionDeclarationDict,
    ToolListUnionDict,
    ToolConfigDict,
]):

    def __init__(self, config: GoogleConfig):
        super().__init__()
        self._format = GoogleFormat(config)

    @property
    @override
    def format(self) -> GoogleFormat:
        return self._format
