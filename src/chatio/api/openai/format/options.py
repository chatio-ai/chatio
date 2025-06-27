
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionPredictionContentParam

from chatio.core.models import ChatOptions
from chatio.core.models import PredictContent
from chatio.core.models import SystemContent

from chatio.core.format.options import ApiFormatOptions

from chatio.api.openai.params import OpenAIParamsOptions
from chatio.api.openai.config import OpenAIConfig


class OpenAIFormatOptions(ApiFormatOptions[
    ChatCompletionContentPartTextParam,
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

    def system_content(self, content: ChatCompletionContentPartTextParam) -> ChatCompletionMessageParam:
        if content['type'] != 'text':
            raise TypeError

        if self._config.options.legacy:
            return {
                "role": "system",
                "content": content['text'],
            }

        return {
            "role": "developer",
            "content": [content],
        }

    @override
    def format(self, options: ChatOptions) -> OpenAIParamsOptions:
        _options = OpenAIParamsOptions()

        for option in options.values():
            match option:
                case SystemContent(text):
                    _options.system = self.system_content(self.text_message(text))
                case PredictContent(text):
                    if self._config.options.prediction:
                        _options.prediction = self.prediction_content(self.text_message(text))
                case _:
                    pass

        return _options
