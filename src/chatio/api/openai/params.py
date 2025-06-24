
from dataclasses import dataclass

from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.params import ApiParams


from .config import OpenAIConfig
from .format import OpenAIFormat


@dataclass(init=False)
class OpenAIParams(ApiParams[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    def __init__(self, config: OpenAIConfig):
        super().__init__()
        self._format = OpenAIFormat(config)

    @property
    @override
    def format(self) -> OpenAIFormat:
        return self._format
