
from abc import ABC, abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiExtras
from chatio.core.params import ApiFields
from chatio.core.params import ApiParams

from .extra import ApiFormatExtra
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

    def spawn(self, state: ChatState, tools: ChatTools) -> ApiFields[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolSelectionT,
        ApiExtrasT,
    ]:
        return ApiFields(
            system=self._format_state.system(state.system),
            messages=self._format_state.messages(state.messages),
            extras=self._format_extra.build(state.extras),
            tools=self._format_tools.tools(tools.tools),
            tool_choice=self._format_tools.tool_choice(tools.tool_choice),
        )

    @property
    @abstractmethod
    def _format_state(self) -> ApiFormatState[
        SystemContentT,
        MessageContentT,
        TextMessageT,
        ImageDocumentT,
        TextDocumentT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_extra(self) -> ApiFormatExtra[
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
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams:
        ...
