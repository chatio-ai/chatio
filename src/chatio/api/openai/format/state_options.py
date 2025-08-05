
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.models import SystemMessage
from chatio.core.models import PredictionMessage
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

    def _prediction_message(self, msg: PredictionMessage | None,
                            ) -> ChatCompletionPredictionContentParam | NotGiven:

        if not self._config.prediction:
            return NOT_GIVEN

        if not msg:
            return NOT_GIVEN

        content = message_text(msg)

        return {
            "type": "content",
            "content": [content],
        }

    def _system_message(self, msg: SystemMessage | None) -> list[ChatCompletionMessageParam]:

        if not msg:
            return []

        content = message_text(msg)

        if self._config.compat:
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
        return OpenAIStateOptions(
            system=self._system_message(options.system),
            prediction=self._prediction_message(options.prediction),
        )
