
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.claude.config import ClaudeConfigFormat
from chatio.api.claude.params import ClaudeParams

from .state_messages import ClaudeMessagesFormatter
from .state_options import ClaudeOptionsFormatter
from .tools import ClaudeToolsFormatter


# pylint: disable=too-few-public-methods
class ClaudeFormat(ApiFormat[
    ClaudeParams,
]):

    def __init__(self, config: ClaudeConfigFormat) -> None:
        self._messages_formatter = ClaudeMessagesFormatter(config)
        self._options_formatter = ClaudeOptionsFormatter(config)
        self._tools_formatter = ClaudeToolsFormatter(config)

    @override
    def format(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        # pylint: disable=unexpected-keyword-arg
        return ClaudeParams(
            messages=self._messages_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tools_formatter.format(tools),
        )
