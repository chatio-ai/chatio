
from abc import abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParams
from chatio.core.config import ApiConfigFormat

from ._common import ApiFormatBase

from .history import ApiFormatHistoryProto
from .options import ApiFormatOptionsProto
from .tooling import ApiFormatToolingProto


class ApiFormat[
    MessageContentT,
    ApiStateOptionsT: ApiStateOptions,
    ToolDefinitionsT,
    ToolChoiceT,
    ApiConfigFormatT: ApiConfigFormat,
](
    ApiFormatBase[ApiConfigFormatT],
):

    @property
    @abstractmethod
    def _format_history(self) -> ApiFormatHistoryProto[MessageContentT]:
        ...

    @property
    @abstractmethod
    def _format_options(self) -> ApiFormatOptionsProto[ApiStateOptionsT]:
        ...

    @property
    @abstractmethod
    def _format_tooling(self) -> ApiFormatToolingProto[ToolDefinitionsT, ToolChoiceT]:
        ...

    def format(self, state: ChatState, tools: ChatTools) -> ApiParams[
        MessageContentT,
        ApiStateOptionsT,
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        return ApiParams(
            messages=self._format_history.format(state.messages),
            options=self._format_options.format(state.options),
            tools=self._format_tooling.format(tools),
        )
