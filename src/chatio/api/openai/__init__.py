
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core import ApiIfaces


from .config import OpenAIConfig
from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIApi(ApiIfaces[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    def __init__(self, config: OpenAIConfig) -> None:
        self._config = config

        self._params = OpenAIParams()
        self._format = OpenAIFormat(config)
        self._client = OpenAIClient(config)

    @property
    @override
    def config(self) -> OpenAIConfig:
        return self._config

    @property
    @override
    def params(self) -> OpenAIParams:
        return self._params

    @property
    @override
    def format(self) -> OpenAIFormat:
        return self._format

    @property
    @override
    def client(self) -> OpenAIClient:
        return self._client
