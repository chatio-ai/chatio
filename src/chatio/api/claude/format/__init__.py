
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.claude.config import ClaudeFormatConfig
from chatio.api.claude.params import ClaudeParams

from .state_messages import ClaudeMessagesFormat
from .state_options import ClaudeOptionsFormat
from .tools import ClaudeToolsFormat


# pylint: disable=too-few-public-methods
class ClaudeFormat(ApiFormat[
    ClaudeParams,
]):

    def __init__(self, config: ClaudeFormatConfig) -> None:
        self._messages_format = ClaudeMessagesFormat(use_cache=config.use_cache)
        self._options_format = ClaudeOptionsFormat(use_cache=config.use_cache)
        self._tools_format = ClaudeToolsFormat(use_cache=config.use_cache)

    @override
    def __call__(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        return ClaudeParams(
            messages=self._messages_format(state.messages),
            options=self._options_format(state.options),
            tools=self._tools_format(tools),
        )
