
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.openai.config import OpenAIConfigFormat
from chatio.api.openai.params import OpenAIParams

from .state_messages import OpenAIMessagesFormatter
from .state_options import OpenAIOptionsFormatter
from .tools import OpenAIToolsFormatter


# pylint: disable=too-few-public-methods
class OpenAIFormat(ApiFormat[
    OpenAIConfigFormat,
    OpenAIParams,
]):

    def __init__(self, config: OpenAIConfigFormat) -> None:
        super().__init__(config)
        self._messages_formatter = OpenAIMessagesFormatter(self._config)
        self._options_formatter = OpenAIOptionsFormatter(self._config)
        self._tools_formatter = OpenAIToolsFormatter(self._config)

    @override
    def format(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        # pylint: disable=unexpected-keyword-arg
        return OpenAIParams(
            messages=self._messages_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tools_formatter.format(tools),
        )
