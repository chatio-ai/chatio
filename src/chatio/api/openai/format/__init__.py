
from typing import override

from openai.types.chat import ChatCompletionMessageParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NotGiven


from chatio.core.format import ApiFormat

from chatio.api.openai.params import OpenAIStateOptions
from chatio.api.openai.config import OpenAIConfigFormat

from .state_messages import OpenAIMessagesFormatter
from .state_options import OpenAIOptionsFormatter
from .tools import OpenAIToolsFormatter


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
    def _messages_formatter(self) -> OpenAIMessagesFormatter:
        return OpenAIMessagesFormatter(self._config)

    @property
    @override
    def _options_formatter(self) -> OpenAIOptionsFormatter:
        return OpenAIOptionsFormatter(self._config)

    @property
    @override
    def _tools_formatter(self) -> OpenAIToolsFormatter:
        return OpenAIToolsFormatter(self._config)
