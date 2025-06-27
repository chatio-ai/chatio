
from dataclasses import dataclass

from anthropic.types import MessageParam
from anthropic.types import TextBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.params import ApiParamsOptions
from chatio.core.params import ApiParams


class ClaudeParamsOptions(ApiParamsOptions, total=False):
    system: TextBlockParam | None


@dataclass
class ClaudeParams(ApiParams):
    max_tokens: int

    messages: list[MessageParam]

    system: list[TextBlockParam] | NotGiven = NOT_GIVEN

    tools: list[ToolParam] | NotGiven = NOT_GIVEN

    tool_choice: ToolChoiceParam | NotGiven = NOT_GIVEN
