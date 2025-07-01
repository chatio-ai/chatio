
from typing import override

from openai.types.chat import ChatCompletionMessageParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NotGiven


from chatio.core.format import ApiFormat

from chatio.api.openai.params import OpenAIStateOptions
from chatio.api.openai.config import OpenAIConfigFormat

from .history import OpenAIHistoryFormatter
from .options import OpenAIOptionsFormatter
from .tooling import OpenAIToolingFormatter


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
    def _history_formatter(self) -> OpenAIHistoryFormatter:
        return OpenAIHistoryFormatter(self._config)

    @property
    @override
    def _options_formatter(self) -> OpenAIOptionsFormatter:
        return OpenAIOptionsFormatter(self._config)

    @property
    @override
    def _tooling_formatter(self) -> OpenAIToolingFormatter:
        return OpenAIToolingFormatter(self._config)
