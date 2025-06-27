
from typing import override

from anthropic.types import MessageParam

from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import DocumentBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NOT_GIVEN


from chatio.core.params import ApiExtras
from chatio.core.format import ApiFormat

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.api.claude.config import ClaudeConfig
from chatio.api.claude.params import ClaudeParams

from .state import ClaudeFormatState
from .state import ClaudeFormatExtra
from .tools import ClaudeFormatTools


class ClaudeFormat(ApiFormat[
    TextBlockParam,
    MessageParam,
    TextBlockParam,
    ImageBlockParam,
    DocumentBlockParam,
    ToolParam,
    list[ToolParam],
    ToolChoiceParam,
    ApiExtras,
    ClaudeConfig,
]):

    @property
    @override
    def _format_extra(self) -> ClaudeFormatExtra:
        return ClaudeFormatExtra(self._config)

    @property
    @override
    def _format_state(self) -> ClaudeFormatState:
        return ClaudeFormatState(self._config)

    @property
    @override
    def _format_tools(self) -> ClaudeFormatTools:
        return ClaudeFormatTools(self._config)

    @override
    def build(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        fields = self.spawn(state, tools)

        _system = NOT_GIVEN if fields.system is None else [fields.system]

        _tools = NOT_GIVEN if fields.tools is None else fields.tools
        _tool_choice = NOT_GIVEN if fields.tool_choice is None else fields.tool_choice

        return ClaudeParams(
            max_tokens=4096,
            system=_system,
            messages=fields.messages,
            tools=_tools,
            tool_choice=_tool_choice,
        )
