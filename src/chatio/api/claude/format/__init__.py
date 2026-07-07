
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.claude.config import ClaudeFormatConfig
from chatio.api.claude.params import ClaudeParams

from .state_messages import ClaudeMessagesFormatter
from .state_options import ClaudeOptionsFormatter
from .tools import ClaudeToolsFormatter


# pylint: disable=too-few-public-methods
class ClaudeFormat(ApiFormat[
    ClaudeParams,
]):

    def __init__(self, config: ClaudeFormatConfig) -> None:
        self._messages_formatter = ClaudeMessagesFormatter(use_cache=config.use_cache)
        self._options_formatter = ClaudeOptionsFormatter(use_cache=config.use_cache)
        self._tools_formatter = ClaudeToolsFormatter(use_cache=config.use_cache)

    @override
    def format(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        # pylint: disable=unexpected-keyword-arg
        return ClaudeParams(
            messages=self._messages_formatter.format(state.messages),
            options=self._options_formatter.format(state.options),
            tools=self._tools_formatter.format(tools),
        )
