
from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven


from chatio.core.format import ApiFormat

from chatio.api.claude.params import ClaudeStateOptions
from chatio.api.claude.config import ClaudeConfigFormat

from .state_messages import ClaudeMessagesFormatter
from .state_options import ClaudeOptionsFormatter
from .tools import ClaudeToolsFormatter


# pylint: disable=too-few-public-methods
class ClaudeFormat(ApiFormat[
    MessageParam,
    ClaudeStateOptions,
    list[ToolParam] | NotGiven,
    ToolChoiceParam | NotGiven,
    ClaudeConfigFormat,
]):

    @property
    @override
    def _messages_formatter(self) -> ClaudeMessagesFormatter:
        return ClaudeMessagesFormatter(self._config)

    @property
    @override
    def _options_formatter(self) -> ClaudeOptionsFormatter:
        return ClaudeOptionsFormatter(self._config)

    @property
    @override
    def _tools_formatter(self) -> ClaudeToolsFormatter:
        return ClaudeToolsFormatter(self._config)
