
from dataclasses import dataclass

from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam


from chatio.core.params import ApiParams


from .config import ClaudeConfig
from .format import ClaudeFormat


@dataclass(init=False)
class ClaudeParams(ApiParams[
    TextBlockParam,
    MessageParam,
    None,
    TextBlockParam,
    ImageBlockParam,
    ToolParam,
    list[ToolParam],
    ToolChoiceParam,
]):

    def __init__(self, config: ClaudeConfig):
        super().__init__()
        self._format = ClaudeFormat(config)

    @property
    @override
    def format(self) -> ClaudeFormat:
        return self._format
