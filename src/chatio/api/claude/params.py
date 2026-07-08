
from dataclasses import dataclass

from anthropic.types import TextBlockParam

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import Omit, omit


@dataclass
class ClaudeParams:
    messages: list[MessageParam]
    system: list[TextBlockParam] | Omit = omit
    tools: list[ToolParam] | Omit = omit
    tool_choice: ToolChoiceParam | Omit = omit
