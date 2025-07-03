
from typing import override

from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionPredictionContentParam

from chatio.core.models import ChatOptions
from chatio.core.models import PredictMessage

from chatio.core.format.options import ApiFormatOptions

from chatio.api.openai.params import OpenAIParamsOptions
from chatio.api.openai.config import OpenAIConfig


class OpenAIFormatOptions(ApiFormatOptions[
    OpenAIParamsOptions,
    OpenAIConfig,
]):

    def text_message(self, text: str) -> ChatCompletionContentPartTextParam:
        return {
            "type": "text",
            "text": text,
        }

    def prediction_content(
        self, content: ChatCompletionContentPartTextParam,
    ) -> ChatCompletionPredictionContentParam:

        return {
            "type": "content",
            "content": [content],
        }

    @override
    def index(self) -> list[str]:
        return ['prediction']

    @override
    def format(self, options: ChatOptions) -> OpenAIParamsOptions:
        _options: OpenAIParamsOptions = {}

        for option in options.values():
            match option:
                case PredictMessage(text):
                    if self._config.options.prediction:
                        _options.update({'prediction': self.prediction_content(self.text_message(text))})
                case _:
                    pass

        return _options
