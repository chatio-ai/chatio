
from dataclasses import dataclass

from anthropic.types import MessageParam
from anthropic.types import TextBlockParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.params import ApiParams


@dataclass
class ClaudeParams(ApiParams):

    messages: list[MessageParam]

    system: list[TextBlockParam] | NotGiven = NOT_GIVEN

    tools: list[ToolParam] | NotGiven = NOT_GIVEN

    tool_choice: ToolChoiceParam | NotGiven = NOT_GIVEN
