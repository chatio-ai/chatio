
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
        return OpenAIParams(
            messages=self._messages_format(state.messages),
            options=self._options_format(state.options),
            tools=self._tools_format(tools),
        )
