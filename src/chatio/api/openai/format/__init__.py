
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

from chatio.api.openai.params import OpenAIParamsOptions
from chatio.api.openai.params import OpenAIParams
from chatio.api.openai.config import OpenAIConfig

from .history import OpenAIFormatHistory
from .options import OpenAIFormatOptions
from .tooling import OpenAIFormatTooling


class OpenAIFormat(ApiFormat[
    ChatCompletionMessageParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    File,
    list[ChatCompletionToolParam],
    ChatCompletionToolParam,
    ChatCompletionToolChoiceOptionParam,
    OpenAIParamsOptions,
    OpenAIConfig,
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

    @override
    def build(self, state: ChatState, tools: ChatTools) -> OpenAIParams:
        params = self.spawn(state, tools)

        if params.options is None:
            params.options = {}

        _messages = params.messages
        _system = params.options.get('system')
        if _system is not None:
            _messages = [_system, *_messages]

        _prediction = params.options.get('prediction')
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
