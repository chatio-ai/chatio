
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.models import ChatStateOptions

from chatio.core.format.state_options import ApiOptionsFormatterBase

from chatio.api.openai.params import OpenAIStateOptions
from chatio.api.openai.config import OpenAIConfigFormat

from .state_messages import message_text


# pylint: disable=too-few-public-methods
class OpenAIOptionsFormatter(ApiOptionsFormatterBase[
    OpenAIStateOptions,
    OpenAIConfigFormat,
]):

    def _prediction_message(
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

    def _system_message(
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
    def format(self, options: ChatStateOptions) -> OpenAIStateOptions:

        text = None if options.system is None else message_text(options.system.text)
        _system = self._system_message(text)

        text = None if options.prediction is None else message_text(options.prediction.text)
        _prediction = self._prediction_message(text)

        return OpenAIStateOptions(
            system=_system,
            prediction=_prediction,
        )
