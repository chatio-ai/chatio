
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.config import ApiHelper
from chatio.core.config import ModelConfig


from .config import OpenAIConfig
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIApi(ApiHelper[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    def __init__(self, model: ModelConfig, config: OpenAIConfig):
        self._model = model

        # params = OpenAIParams(**config.config.options if config.config.options else {})

        self._format = OpenAIFormat(config)
        self._client = OpenAIClient(config)

    @property
    @override
    def config(self) -> ModelConfig:
        return self._model

    @property
    @override
    def format(self) -> OpenAIFormat:
        return self._format

    @property
    @override
    def client(self) -> OpenAIClient:
        return self._client
