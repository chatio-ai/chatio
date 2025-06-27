
from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat.chat_completion_content_part_param import File

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NOT_GIVEN


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
    OpenAIConfig,
]):

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

    @override
    def build(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        params = self.spawn(state, tools)

        _system = [] if params.system is None else [params.system]
        _messages = _system + params.messages

        if params.extras is None:
            params.extras = {}

        _prediction = params.extras.get('prediction')
        if _prediction is not None:
            return OpenAIParams(
                messages=_messages,
                prediction=_prediction,
            )

        _tools = NOT_GIVEN if params.tools is None else params.tools
        _tool_choice = NOT_GIVEN if params.tool_choice is None else params.tool_choice

        return OpenAIParams(
            max_completion_tokens=4096,
            messages=_messages,
            tools=_tools,
            tool_choice=_tool_choice,
        )
