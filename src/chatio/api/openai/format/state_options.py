
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai import Omit, omit


from chatio.core.models import SystemMessage
from chatio.core.models import PredictionMessage

from .state_messages import message_text


# pylint: disable=too-few-public-methods
class OpenAIOptionsFormat:

    def __init__(self, *, prediction: bool, compat: bool) -> None:
        self._prediction = prediction
        self._compat = compat

    def prediction_message(
            self, msg: PredictionMessage | None) -> ChatCompletionPredictionContentParam | Omit:

        if not self._prediction:
            return omit

        if not msg:
            return omit

        content = message_text(msg)

        return {
            "type": "content",
            "content": [content],
        }

    def system_message(self, msg: SystemMessage | None) -> list[ChatCompletionMessageParam]:

        if not msg:
            return []

        content = message_text(msg)

        if self._compat:
            return [{
                "role": "system",
                "content": content['text'],
            }]

        return [{
            "role": "developer",
            "content": [content],
        }]
