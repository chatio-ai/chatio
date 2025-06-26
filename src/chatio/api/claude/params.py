
from dataclasses import dataclass

from anthropic.types import MessageParam
from anthropic.types import TextBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam


from chatio.core.params import ApiParams


@dataclass
class ClaudeParams(ApiParams[
    TextBlockParam,
    MessageParam,
    None,
    list[ToolParam],
    ToolChoiceParam,
]):
    pass
