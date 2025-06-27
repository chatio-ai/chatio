
from typing import override

from anthropic.types import MessageParam

from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import DocumentBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam


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
]):

    def __init__(self, config: ClaudeConfig) -> None:
        self._config = config

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

    def build(self, state: ChatState, tools: ChatTools) -> ClaudeParams:
        params = ClaudeParams()
        self.setup(params, state, tools)
        return params
