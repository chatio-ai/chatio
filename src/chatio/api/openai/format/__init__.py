
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.openai.config import OpenAIFormatConfig
from chatio.api.openai.params import OpenAIParams

from .state_messages import OpenAIMessagesFormat
from .state_options import OpenAIOptionsFormat
from .tools import OpenAIToolsFormat


# pylint: disable=too-few-public-methods
class OpenAIFormat(ApiFormat[
    OpenAIParams,
]):

    def __init__(self, config: OpenAIFormatConfig) -> None:
        self._messages_format = OpenAIMessagesFormat(compat=config.compat)
        self._options_format = OpenAIOptionsFormat(
            prediction=config.prediction, compat=config.compat)
        self._tools_format = OpenAIToolsFormat()

    @override
    def __call__(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        tools_ = self._tools_format(tools)

        return OpenAIParams(
            messages=self._messages_format(state.messages),
            system=self._options_format.system_message(state.options.system),
            tools=tools_.tools,
            tool_choice=tools_.tool_choice,
            prediction=self._options_format.prediction_message(state.options.prediction),
        )
