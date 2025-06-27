
from typing import override

from anthropic.types import MessageParam

from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import DocumentBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NOT_GIVEN


from chatio.core.format import ApiFormat

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiParamsOptions
from chatio.api.claude.params import ClaudeParams
from chatio.api.claude.config import ClaudeConfig

from .history import ClaudeFormatHistory
from .options import ClaudeFormatOptions
from .tooling import ClaudeFormatTooling


class ClaudeFormat(ApiFormat[
    TextBlockParam,
    MessageParam,
    TextBlockParam,
    ImageBlockParam,
    DocumentBlockParam,
    list[ToolParam],
    ToolParam,
    ToolChoiceParam,
    ApiParamsOptions,
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

    @override
    def build(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        params = self.spawn(state, tools)

        _system = NOT_GIVEN if params.system is None else [params.system]

        _tools = NOT_GIVEN if params.tools is None else params.tools
        _tool_choice = NOT_GIVEN if params.tool_choice is None else params.tool_choice

        return ClaudeParams(
            max_tokens=4096,
            system=_system,
            messages=params.messages,
            tools=_tools,
            tool_choice=_tool_choice,
        )
