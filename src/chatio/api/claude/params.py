
from dataclasses import dataclass

from typing import override

from anthropic.types import MessageParam

from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import DocumentBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam


from chatio.core.params import ApiParamsBuilder
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


class ClaudeParamsBuilder(ApiParamsBuilder[
    TextBlockParam,
    MessageParam,
    None,
    TextBlockParam,
    ImageBlockParam,
    DocumentBlockParam,
    ToolParam,
    list[ToolParam],
    ToolChoiceParam,
]):

    @override
    def spawn(self) -> ClaudeParams:
        return ClaudeParams()

    @override
    def build(self) -> ClaudeParams:
        params = self.spawn()
        self.setup(params)
        return params
