
from dataclasses import dataclass, field

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.params import ApiStateOptions


@dataclass
class OpenAIStateOptions(ApiStateOptions):
    system: list[ChatCompletionMessageParam] = field(default_factory=list)

    prediction: ChatCompletionPredictionContentParam | NotGiven = NOT_GIVEN
