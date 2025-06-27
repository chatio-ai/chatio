
from abc import abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.config import ApiConfig
from chatio.core.params import ApiExtras

from chatio.core.params import ApiParamsGeneric
from chatio.core.params import ApiParams

from ._common import ApiFormatBase

from .history import ApiFormatHistory
from .options import ApiFormatOptions
from .tooling import ApiFormatTooling


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
    def _format_history(self) -> ApiFormatHistory[
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
    def _format_options(self) -> ApiFormatOptions[
        ApiExtrasT,
        ApiConfigT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_tooling(self) -> ApiFormatTooling[
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
            system=self._format_history.system(state.system),
            messages=self._format_history.messages(state.messages),
            extras=self._format_options.build(state.extras),
            tools=self._format_tooling.tools(tools.tools),
            tool_choice=self._format_tooling.tool_choice(tools.tool_choice),
        )

    @abstractmethod
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams:
        ...
