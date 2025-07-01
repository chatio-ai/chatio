
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.models import StateOptions

from chatio.core.format.options import ApiOptionsFormatterBase

from chatio.api.openai.params import OpenAIStateOptions
from chatio.api.openai.config import OpenAIConfigFormat


def text_message(text: str) -> ChatCompletionContentPartTextParam:
    return {
        "type": "text",
        "text": text,
    }


# pylint: disable=too-few-public-methods
class OpenAIOptionsFormatter(ApiOptionsFormatterBase[
    OpenAIStateOptions,
    OpenAIConfigFormat,
]):

    def _prediction_content(
        self, content: ChatCompletionContentPartTextParam | None,
    ) -> ChatCompletionPredictionContentParam | NotGiven:

        if not self._config.prediction:
            return NOT_GIVEN

        if content is None:
            return NOT_GIVEN

        return {
            "type": "content",
            "content": [content],
        }

    def _system_content(
        self, content: ChatCompletionContentPartTextParam | None,
    ) -> list[ChatCompletionMessageParam]:

        if content is None:
            return []

        if content['type'] != 'text':
            raise TypeError

        if self._config.legacy:
            return [{
                "role": "system",
                "content": content['text'],
            }]

        return [{
            "role": "developer",
            "content": [content],
        }]

    @override
    def format(self, options: StateOptions) -> OpenAIStateOptions:

        text = None if options.system is None else text_message(options.system.text)
        _system = self._system_content(text)

        text = None if options.prediction is None else text_message(options.prediction.text)
        _prediction = self._prediction_content(text)

        return OpenAIStateOptions(
            system=_system,
            prediction=_prediction,
        )
