
from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam

# from chatio.core.params import SystemMessage
from chatio.core.params import OutputMessage
from chatio.core.params import InputMessage

from chatio.core.params import ImageDocument
from chatio.core.params import CallResponse
from chatio.core.params import CallRequest

# from chatio.core.params import ToolChoice

from chatio.core.params import ApiParams

from .format import ClaudeFormat


class ClaudeParams:
    def __init__(self, params: ApiParams, formatter: ClaudeFormat):
        self._params = params
        self._format = formatter

    @property
    def system(self) -> TextBlockParam | None:
        if self._params.system is None:
            return None

        return self._format.system_content(self._format.text_chunk(self._params.system.text))

    @property
    def messages(self) -> list[MessageParam]:
        messages = []

        for message in self._params.messages:
            match message:
                case InputMessage(text):
                    messages.append(self._format.input_message(text))
                case OutputMessage(text):
                    messages.append(self._format.output_message(text))
                case CallRequest(tool_call_id, tool_name, tool_input):
                    messages.append(self._format.call_request(tool_call_id, tool_name, tool_input))
                case CallResponse(tool_call_id, tool_name, tool_output):
                    messages.append(self._format.call_response(tool_call_id, tool_name, tool_output))
                case ImageDocument(blob, mimetype):
                    messages.append(self._format.image_document(blob, mimetype))
                case _:
                    raise RuntimeError(message)

        return self._format.chat_messages(messages)

    @property
    def tools(self) -> list[ToolParam] | None:
        if self._params.tools is None:
            return None

        _tool_definitions = \
            [self._format.tool_definition(tool.name, tool.desc, tool.schema) for tool in self._params.tools]

        return self._format.tool_definitions(_tool_definitions)

    @property
    def tool_choice(self) -> ToolChoiceParam | None:
        if self._params.tool_choice is None:
            return None

        return self._format.tool_selection(
            self._params.tool_choice.mode, self._params.tool_choice.name, self._params.tool_choice.tools)
