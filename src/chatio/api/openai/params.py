
from dataclasses import dataclass

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.params import ApiParamsOptions
from chatio.core.params import ApiParams


@dataclass
class OpenAIParamsOptions(ApiParamsOptions):
    system: ChatCompletionMessageParam | None = None

    prediction: ChatCompletionPredictionContentParam | None = None


@dataclass
class OpenAIParams(ApiParams):
    messages: list[ChatCompletionMessageParam]

    max_completion_tokens: int | NotGiven = NOT_GIVEN

    prediction: ChatCompletionPredictionContentParam | NotGiven = NOT_GIVEN

    tools: list[ChatCompletionToolParam] | NotGiven = NOT_GIVEN

    tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN
