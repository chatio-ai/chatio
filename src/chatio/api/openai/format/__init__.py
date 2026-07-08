
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.openai.config import OpenAIFormatConfig
from chatio.api.openai.params import OpenAIParams

from .state import OpenAIChatMessagesFormat
from .state import OpenAISystemMessageFormat
from .state import OpenAIPredictionMessageFormat
from .tools import OpenAIToolSchemasFormat
from .tools import OpenAIToolChoiceFormat


# pylint: disable=too-few-public-methods
class OpenAIFormat(ApiFormat[
    OpenAIParams,
]):

    def __init__(self, config: OpenAIFormatConfig) -> None:
        self._chat_messages_format = OpenAIChatMessagesFormat(compat=config.compat)
        self._system_message_format = OpenAISystemMessageFormat(compat=config.compat)
        self._prediction_message_format = OpenAIPredictionMessageFormat(
                prediction=config.prediction)
        self._tool_schemas_format = OpenAIToolSchemasFormat()
        self._tool_choice_format = OpenAIToolChoiceFormat()

    @override
    def __call__(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        return OpenAIParams(
            messages=self._chat_messages_format(state.messages),
            system=self._system_message_format(state.system),
            tools=self._tool_schemas_format(tools.schemas),
            tool_choice=self._tool_choice_format(tools.choice),
            prediction=self._prediction_message_format(state.prediction),
        )
