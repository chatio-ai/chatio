
from abc import abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.config import ApiConfig
from chatio.core.params import ApiExtras

from chatio.core.params import ApiParamsGeneric
from chatio.core.params import ApiParams

from ._common import ApiFormatBase

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
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
):

    @property
    @abstractmethod
    def _format_state(self) -> ApiFormatState[
        SystemContentT,
        MessageContentT,
        TextMessageT,
        ImageDocumentT,
        TextDocumentT,
        ApiConfigT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_extra(self) -> ApiFormatExtra[
        ApiExtrasT,
        ApiConfigT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_tools(self) -> ApiFormatTools[
        ToolDefinitionT,
        ToolDefinitionsT,
        ToolSelectionT,
        ApiConfigT,
    ]:
        ...

    def spawn(self, state: ChatState, tools: ChatTools) -> ApiParamsGeneric[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolSelectionT,
        ApiExtrasT,
    ]:
        return ApiParamsGeneric(
            system=self._format_state.system(state.system),
            messages=self._format_state.messages(state.messages),
            extras=self._format_extra.build(state.extras),
            tools=self._format_tools.tools(tools.tools),
            tool_choice=self._format_tools.tool_choice(tools.tool_choice),
        )

    @abstractmethod
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams:
        ...
