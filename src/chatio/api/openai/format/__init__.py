
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat.chat_completion_content_part_param import File

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.format import ApiFormat

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.api.openai.config import OpenAIConfig
from chatio.api.openai.params import OpenAIExtras
from chatio.api.openai.params import OpenAIParams

from .state import OpenAIFormatState
from .state import OpenAIFormatExtra
from .tools import OpenAIFormatTools


class OpenAIFormat(ApiFormat[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    File,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
    OpenAIExtras,
]):
    def __init__(self, config: OpenAIConfig) -> None:
        self._config = config

    @property
    @override
    def _format_extra(self) -> OpenAIFormatExtra:
        return OpenAIFormatExtra(self._config)

    @property
    @override
    def _format_state(self) -> OpenAIFormatState:
        return OpenAIFormatState(self._config)

    @property
    @override
    def _format_tools(self) -> OpenAIFormatTools:
        return OpenAIFormatTools(self._config)

    def build(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        params = OpenAIParams()
        self.setup(params, state, tools)
        return params
