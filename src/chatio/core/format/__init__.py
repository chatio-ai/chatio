
from abc import abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiParamsOptions
from chatio.core.params import ApiParamsGeneric
from chatio.core.params import ApiParams
from chatio.core.config import ApiConfig

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
    ToolDefinitionsT,
    ToolSchemaT,
    ToolChoiceT,
    ApiParamsOptionsT: ApiParamsOptions,
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
        ApiParamsOptionsT,
        ApiConfigT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_tooling(self) -> ApiFormatTooling[
        ToolDefinitionsT,
        ToolSchemaT,
        ToolChoiceT,
        ApiConfigT,
    ]:
        ...

    def spawn(self, state: ChatState, tools: ChatTools) -> ApiParamsGeneric[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolChoiceT,
        ApiParamsOptionsT,
    ]:
        return ApiParamsGeneric(
            system=self._format_history.system(state.system),
            messages=self._format_history.messages(state.messages),
            options=self._format_options.format(state.options),
            tools=self._format_tooling.tools(tools.tools),
            tool_choice=self._format_tooling.tool_choice(tools.tool_choice),
        )

    @abstractmethod
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams:
        ...
