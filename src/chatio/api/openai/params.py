
from dataclasses import dataclass, field

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParamsImpl


@dataclass
class OpenAIStateOptions(ApiStateOptions):
    system: list[ChatCompletionMessageParam] = field(default_factory=list)

    prediction: ChatCompletionPredictionContentParam | NotGiven = NOT_GIVEN


@dataclass
class OpenAIParams(ApiParamsImpl[
    ChatCompletionMessageParam,
    OpenAIStateOptions,
    list[ChatCompletionToolParam] | NotGiven,
    ChatCompletionToolChoiceOptionParam | NotGiven,
]):
    pass
