
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.google.config import GoogleFormatConfig
from chatio.api.google.params import GoogleParams

from .state_messages import GoogleMessagesFormatter
from .state_options import GoogleOptionsFormatter
from .tools import GoogleToolsFormatter


# pylint: disable=too-few-public-methods
class GoogleFormat(ApiFormat[
    GoogleParams,
]):

    def __init__(self, config: GoogleFormatConfig) -> None:
        self._messages_formatter = GoogleMessagesFormatter()
        self._options_formatter = GoogleOptionsFormatter()
        self._tools_formatter = GoogleToolsFormatter(grounding=config.grounding)

    @override
    def format(self, state: ChatState, tools: ChatTools) -> GoogleParams:
        # pylint: disable=unexpected-keyword-arg
        return GoogleParams(
            messages=self._messages_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tools_formatter.format(tools),
        )
