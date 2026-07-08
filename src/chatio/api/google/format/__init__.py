
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.google.config import GoogleFormatConfig
from chatio.api.google.params import GoogleParams

from .state import GoogleSystemMessageFormat
from .state import GoogleChatMessagesFormat
from .tools import GoogleToolSchemasFormat
from .tools import GoogleToolChoiceFormat


# pylint: disable=too-few-public-methods
class GoogleFormat(ApiFormat[
    GoogleParams,
]):

    def __init__(self, config: GoogleFormatConfig) -> None:
        self._chat_messages_format = GoogleChatMessagesFormat()
        self._system_message_format = GoogleSystemMessageFormat()
        self._tool_schemas_format = GoogleToolSchemasFormat(grounding=config.grounding)
        self._tool_choice_format = GoogleToolChoiceFormat()

    @override
    def __call__(self, state: ChatState, tools: ChatTools) -> GoogleParams:
        return GoogleParams(
            messages=self._chat_messages_format(state.messages),
            system=self._system_message_format(state.system),
            tools=self._tool_schemas_format(tools.schemas),
            tool_config=self._tool_choice_format(tools.choice),
        )
