
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.config import ChatConfig
from chatio.core.config import ChatApi


from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIApi(ChatApi[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    def __init__(self, config: ChatConfig):
        super().__init__()

        self._config = config

        params = OpenAIParams(**config.config.options if config.config.options else {})

        self._format = OpenAIFormat(params)
        self._client = OpenAIClient(config.config, params, self._format)

    @property
    @override
    def config(self) -> ChatConfig:
        return self._config

    @property
    @override
    def format(self) -> OpenAIFormat:
        return self._format

    @property
    @override
    def client(self) -> OpenAIClient:
        return self._client
