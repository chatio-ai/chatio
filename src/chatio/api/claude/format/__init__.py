
from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven


from chatio.core.format import ApiFormat

from chatio.api.claude.params import ClaudeStateOptions
from chatio.api.claude.config import ClaudeConfig

from .history import ClaudeFormatHistory
from .options import ClaudeFormatOptions
from .tooling import ClaudeFormatTooling


class ClaudeFormat(ApiFormat[
    MessageParam,
    ClaudeStateOptions,
    list[ToolParam] | NotGiven,
    ToolChoiceParam | NotGiven,
    ClaudeConfig,
]):

    @property
    @override
    def _format_history(self) -> ClaudeFormatHistory:
        return ClaudeFormatHistory(self._config)

    @property
    @override
    def _format_options(self) -> ClaudeFormatOptions:
        return ClaudeFormatOptions(self._config)

    @property
    @override
    def _format_tooling(self) -> ClaudeFormatTooling:
        return ClaudeFormatTooling(self._config)
