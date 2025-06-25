
from dataclasses import dataclass

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam


from chatio.core.params import ApiParamsBase


@dataclass
class ClaudeParams(ApiParamsBase[
    TextBlockParam,
    MessageParam,
    list[ToolParam],
    ToolChoiceParam,
    None,
]):
    pass
