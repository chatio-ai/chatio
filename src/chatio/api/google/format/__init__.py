
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
from .state import GoogleFormatExtra
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
    GoogleConfig,
]):

    @property
    @override
    def _format_extra(self) -> GoogleFormatExtra:
        return GoogleFormatExtra(self._config)

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
        fields = self.spawn(state, tools)
        return GoogleParams(
            system=fields.system,
            messages=fields.messages,
            tools=fields.tools,
            tool_config=fields.tool_choice,
        )
