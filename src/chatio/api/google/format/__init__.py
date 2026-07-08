
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.google.config import GoogleFormatConfig
from chatio.api.google.params import GoogleParams

from .state_messages import GoogleMessagesFormat
from .state_options import GoogleOptionsFormat
from .tools import GoogleToolsFormat


# pylint: disable=too-few-public-methods
class GoogleFormat(ApiFormat[
    GoogleParams,
]):

    def __init__(self, config: GoogleFormatConfig) -> None:
        self._messages_format = GoogleMessagesFormat()
        self._options_format = GoogleOptionsFormat()
        self._tools_format = GoogleToolsFormat(grounding=config.grounding)

    @override
    def __call__(self, state: ChatState, tools: ChatTools) -> GoogleParams:
        return GoogleParams(
            messages=self._messages_format(state.messages),
            options=self._options_format(state.options),
            tools=self._tools_format(tools),
        )
