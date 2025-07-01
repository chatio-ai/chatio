
from abc import abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParams
from chatio.core.config import ApiConfigFormat

from ._common import ApiFormatBase

from .history import ApiHistoryFormatter
from .options import ApiOptionsFormatter
from .tooling import ApiToolingFormatter


# pylint: disable=too-few-public-methods
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
    def _history_formatter(self) -> ApiHistoryFormatter[MessageContentT]:
        ...

    @property
    @abstractmethod
    def _options_formatter(self) -> ApiOptionsFormatter[ApiStateOptionsT]:
        ...

    @property
    @abstractmethod
    def _tooling_formatter(self) -> ApiToolingFormatter[ToolDefinitionsT, ToolChoiceT]:
        ...

    def format(self, state: ChatState, tools: ChatTools) -> ApiParams[
        MessageContentT,
        ApiStateOptionsT,
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        return ApiParams(
            messages=self._history_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tooling_formatter.format(tools),
        )
