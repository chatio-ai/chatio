
from dataclasses import dataclass

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from chatio.core.params import ApiExtras
from chatio.core.params import ApiParams


class OpenAIExtras(ApiExtras, total=False):
    prediction: ChatCompletionPredictionContentParam


@dataclass
class OpenAIParams(ApiParams[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
    OpenAIExtras,
]):
    pass
