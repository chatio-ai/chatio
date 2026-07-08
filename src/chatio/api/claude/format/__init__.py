
from typing import override

from chatio.core.models import ChatState
from chatio.core.models import ChatTools
from chatio.core.format import ApiFormat

from chatio.api.claude.config import ClaudeFormatConfig
from chatio.api.claude.params import ClaudeParams

from .state_messages import ClaudeMessagesFormat
from .state_options import ClaudeOptionsFormat
from .tools import ClaudeToolSchemasFormat
from .tools import ClaudeToolChoiceFormat


# pylint: disable=too-few-public-methods
class ClaudeFormat(ApiFormat[
    ClaudeParams,
]):

    def __init__(self, config: ClaudeFormatConfig) -> None:
        self._messages_format = ClaudeMessagesFormat(use_cache=config.use_cache)
        self._options_format = ClaudeOptionsFormat(use_cache=config.use_cache)
        self._tool_schemas_format = ClaudeToolSchemasFormat(use_cache=config.use_cache)
        self._tool_choice_format = ClaudeToolChoiceFormat()

    @override
    def __call__(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        return ClaudeParams(
            messages=self._messages_format(state.messages),
            system=self._options_format.system_message(state.options.system),
            tools=self._tool_schemas_format(tools.schemas),
            tool_choice=self._tool_choice_format(tools.choice),
        )
