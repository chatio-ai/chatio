
from dataclasses import dataclass

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.params import ApiParams


@dataclass(init=False)
class OpenAIParams(ApiParams[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):
    pass
