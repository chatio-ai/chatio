
from abc import ABC, abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiExtras
from chatio.core.params import ApiParams

from .state import ApiFormatState
from .tools import ApiFormatTools


class ApiFormat[
    SystemContentT,
    MessageContentT,
    TextMessageT,
    ImageDocumentT,
    TextDocumentT,
    ToolDefinitionT,
    ToolDefinitionsT,
    ToolSelectionT,
    ApiExtrasT: ApiExtras,
](ABC):

    def setup(self, params: ApiParams[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolSelectionT,
        ApiExtrasT,
    ], state: ChatState, tools: ChatTools):
        params.system = self._format_state.system(state.system)
        params.messages = self._format_state.messages(state.messages)
        params.extras = self._format_state.extras(state.extras)

        params.tools = self._format_tools.tools(tools.tools)
        params.tool_choice = self._format_tools.tool_choice(tools.tool_choice)

    @property
    @abstractmethod
    def _format_state(self) -> ApiFormatState[
        SystemContentT,
        MessageContentT,
        TextMessageT,
        ImageDocumentT,
        TextDocumentT,
        ApiExtrasT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_tools(self) -> ApiFormatTools[
        ToolDefinitionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ]:
        ...

    @abstractmethod
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolSelectionT,
        ApiExtrasT,
    ]:
        ...
