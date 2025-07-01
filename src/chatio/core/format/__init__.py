
from abc import abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParams
from chatio.core.config import ApiConfigFormat

from ._base import ApiFormatBase

from .state_messages import ApiMessagesFormatter
from .state_options import ApiOptionsFormatter
from .tools import ApiToolsFormatter


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
    def _messages_formatter(self) -> ApiMessagesFormatter[MessageContentT]:
        ...

    @property
    @abstractmethod
    def _options_formatter(self) -> ApiOptionsFormatter[ApiStateOptionsT]:
        ...

    @property
    @abstractmethod
    def _tools_formatter(self) -> ApiToolsFormatter[ToolDefinitionsT, ToolChoiceT]:
        ...

    def format(self, state: ChatState, tools: ChatTools) -> ApiParams[
        MessageContentT,
        ApiStateOptionsT,
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        return ApiParams(
            messages=self._messages_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tools_formatter.format(tools),
        )
