
from dataclasses import dataclass

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.mapper import ApiParamsBase


@dataclass
class OpenAIParams(ApiParamsBase[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionPredictionContentParam,
]):
    pass
