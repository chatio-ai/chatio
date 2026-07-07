
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.openai.config import OpenAIFormatConfig
from chatio.api.openai.params import OpenAIParams

from .state_messages import OpenAIMessagesFormatter
from .state_options import OpenAIOptionsFormatter
from .tools import OpenAIToolsFormatter


# pylint: disable=too-few-public-methods
class OpenAIFormat(ApiFormat[
    OpenAIParams,
]):

    def __init__(self, config: OpenAIFormatConfig) -> None:
        self._messages_formatter = OpenAIMessagesFormatter(compat=config.compat)
        self._options_formatter = OpenAIOptionsFormatter(
            prediction=config.prediction, compat=config.compat)
        self._tools_formatter = OpenAIToolsFormatter()

    @override
    def format(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        # pylint: disable=unexpected-keyword-arg
        return OpenAIParams(
            messages=self._messages_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tools_formatter.format(tools),
        )
