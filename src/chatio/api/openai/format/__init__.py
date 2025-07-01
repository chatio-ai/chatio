
from typing import override

from openai.types.chat import ChatCompletionMessageParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NotGiven


from chatio.core.format import ApiFormat

from chatio.api.openai.params import OpenAIStateOptions
from chatio.api.openai.config import OpenAIConfigFormat

from .history import OpenAIFormatHistory
from .options import OpenAIFormatOptions
from .tooling import OpenAIFormatTooling


# pylint: disable=too-few-public-methods
class OpenAIFormat(ApiFormat[
    ChatCompletionMessageParam,
    OpenAIStateOptions,
    list[ChatCompletionToolParam] | NotGiven,
    ChatCompletionToolChoiceOptionParam | NotGiven,
    OpenAIConfigFormat,
]):

    @property
    @override
    def _format_history(self) -> OpenAIFormatHistory:
        return OpenAIFormatHistory(self._config)

    @property
    @override
    def _format_options(self) -> OpenAIFormatOptions:
        return OpenAIFormatOptions(self._config)

    @property
    @override
    def _format_tooling(self) -> OpenAIFormatTooling:
        return OpenAIFormatTooling(self._config)
