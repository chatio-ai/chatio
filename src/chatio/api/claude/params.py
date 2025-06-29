
from dataclasses import dataclass

from anthropic.types import TextBlockParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.params import ApiStateOptions


@dataclass
class ClaudeStateOptions(ApiStateOptions):
    system: list[TextBlockParam] | NotGiven = NOT_GIVEN
