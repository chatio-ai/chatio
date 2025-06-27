
from typing import override

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict
from google.genai.types import PartDict

from google.genai.types import FunctionDeclarationDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.params import ApiExtras
from chatio.core.format import ApiFormat

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.api.google.config import GoogleConfig
from chatio.api.google.params import GoogleParams

from .state import GoogleFormatState
from .tools import GoogleFormatTools


class GoogleFormat(ApiFormat[
    ContentDict,
    ContentUnionDict,
    PartDict,
    PartDict,
    PartDict,
    FunctionDeclarationDict,
    ToolListUnionDict,
    ToolConfigDict,
    ApiExtras,
]):

    def __init__(self, config: GoogleConfig) -> None:
        self._config = config

    @property
    @override
    def _format_state(self) -> GoogleFormatState:
        return GoogleFormatState(self._config)

    @property
    @override
    def _format_tools(self) -> GoogleFormatTools:
        return GoogleFormatTools(self._config)

    @override
    def build(self, state: ChatState, tools: ChatTools) -> GoogleParams:
        params = GoogleParams()
        self.setup(params, state, tools)
        return params
