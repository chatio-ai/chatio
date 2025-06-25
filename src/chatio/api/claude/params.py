
from dataclasses import dataclass

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam


from chatio.core.mapper import ApiParams


@dataclass
class ClaudeParams(ApiParams[
    TextBlockParam,
    MessageParam,
    list[ToolParam],
    ToolChoiceParam,
    None,
]):
    pass
