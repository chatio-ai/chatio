
from dataclasses import dataclass

from anthropic.types import TextBlockParam

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParamsImpl


@dataclass
class ClaudeStateOptions(ApiStateOptions):
    system: list[TextBlockParam] | NotGiven = NOT_GIVEN


@dataclass
class ClaudeParams(ApiParamsImpl[
    MessageParam,
    ClaudeStateOptions,
    list[ToolParam] | NotGiven,
    ToolChoiceParam | NotGiven,
]):
    pass
