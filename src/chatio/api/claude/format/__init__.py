
from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven


from chatio.core.format import ApiFormat

from chatio.api.claude.params import ClaudeStateOptions
from chatio.api.claude.config import ClaudeConfigFormat

from .history import ClaudeHistoryFormatter
from .options import ClaudeOptionsFormatter
from .tooling import ClaudeToolingFormatter


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
    def _history_formatter(self) -> ClaudeHistoryFormatter:
        return ClaudeHistoryFormatter(self._config)

    @property
    @override
    def _options_formatter(self) -> ClaudeOptionsFormatter:
        return ClaudeOptionsFormatter(self._config)

    @property
    @override
    def _tooling_formatter(self) -> ClaudeToolingFormatter:
        return ClaudeToolingFormatter(self._config)
