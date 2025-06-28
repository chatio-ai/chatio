
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionPredictionContentParam

from chatio.core.models import StateOptions

from chatio.core.format.options import ApiFormatOptions

from chatio.api.openai.params import OpenAIStateOptions
from chatio.api.openai.config import OpenAIConfig


class OpenAIFormatOptions(ApiFormatOptions[
    ChatCompletionContentPartTextParam,
    OpenAIStateOptions,
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
    def format(self, options: StateOptions) -> OpenAIStateOptions:
        system = None if options.system is None \
            else self.system_content(self.text_message(options.system.text))

        prediction = None if options.prediction is None \
            else self.prediction_content(self.text_message(options.prediction.text))

        return OpenAIStateOptions(
            system=system,
            prediction=prediction,
        )
