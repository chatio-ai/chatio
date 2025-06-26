
from dataclasses import dataclass

from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat.chat_completion_content_part_param import File

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.params import ApiParamsBuilder
from chatio.core.params import ApiParams


@dataclass
class OpenAIParams(ApiParams[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):
    pass


class OpenAIParamsBuilder(ApiParamsBuilder[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    File,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    @override
    def spawn(self) -> OpenAIParams:
        return OpenAIParams()

    @override
    def build(self) -> OpenAIParams:
        params = self.spawn()
        self.setup(params)
        return params
