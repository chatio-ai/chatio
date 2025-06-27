
from typing import override

from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionPredictionContentParam

from chatio.core.models import ContentEntry
from chatio.core.models import PredictMessage

from chatio.core.format.options import ApiFormatOptions

from chatio.api.openai.params import OpenAIExtras
from chatio.api.openai.config import OpenAIConfig


class OpenAIFormatOptions(ApiFormatOptions[
    OpenAIExtras,
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
    def build(self, extras: dict[str, ContentEntry | None]) -> OpenAIExtras:
        _extras: OpenAIExtras = {}

        for param_name, param in extras.items():
            match param_name:
                case 'prediction' if isinstance(param, PredictMessage):
                    if self._config.options.prediction:
                        _extras['prediction'] = self.prediction_content(self.text_message(param.text))
                case _:
                    pass

        return _extras
