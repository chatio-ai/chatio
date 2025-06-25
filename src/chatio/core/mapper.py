
from chatio.core.models import PredictMessage
from chatio.core.models import SystemMessage
from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument
from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ContentEntry

from chatio.core.params import ApiParamsBase
from chatio.core.params import ApiParams

from chatio.core.format import ApiFormat


class ApiMapper[
    SystemContentT,
    MessageContentT,
    ChatPredictionT,
    TextMessageT,
    ImageDocumentT,
    TextDocumentT,
    ToolDefinitionT,
    ToolDefinitionsT,
    ToolSelectionT,
]:

    def __init__(self, formatter: ApiFormat[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        TextMessageT,
        ImageDocumentT,
        TextDocumentT,
        ToolDefinitionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ]):
        self._format = formatter

    def _system(self, message: SystemMessage | None) -> SystemContentT | None:
        if message is None:
            return None

        return self._format.system_content(self._format.text_message(message.text))

    def _messages(self, messages: list[ContentEntry]) -> list[MessageContentT]:
        _messages = []

        for message in messages:
            match message:
                case InputMessage(text):
                    _messages.append(self._format.input_message(text))
                case OutputMessage(text):
                    _messages.append(self._format.output_message(text))
                case CallRequest(tool_call_id, tool_name, tool_input):
                    _messages.append(self._format.call_request(tool_call_id, tool_name, tool_input))
                case CallResponse(tool_call_id, tool_name, tool_output):
                    _messages.append(self._format.call_response(tool_call_id, tool_name, tool_output))
                case TextDocument(text, mimetype):
                    _messages.append(self._format.text_document(text, mimetype))
                case ImageDocument(blob, mimetype):
                    _messages.append(self._format.image_document(blob, mimetype))
                case _:
                    raise RuntimeError(message)

        return self._format.chat_messages(_messages)

    def _tools(self, tools: list[ToolSchema] | None) -> ToolDefinitionsT | None:
        if tools is None:
            return None

        _tools = [self._format.tool_definition(tool.name, tool.desc, tool.schema) for tool in tools]

        return self._format.tool_definitions(_tools)

    def _tool_choice(self, tool_choice: ToolChoice | None) -> ToolSelectionT | None:
        if tool_choice is None:
            return None

        return self._format.tool_selection(tool_choice.mode, tool_choice.name, tool_choice.tools)

    def _predict(self, message: PredictMessage | None) -> ChatPredictionT | None:
        if message is None:
            return None

        return self._format.prediction_content(self._format.text_message(message.text))

    def map(self, params: ApiParams) -> ApiParamsBase[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolSelectionT,
        ChatPredictionT,
    ]:
        return ApiParamsBase(
            system=self._system(params.system),
            messages=self._messages(params.messages),
            predict=self._predict(params.predict),
            tools=self._tools(params.tools),
            tool_choice=self._tool_choice(params.tool_choice),
        )

    def __call__(self, params: ApiParams) -> ApiParamsBase[
        SystemContentT,
        MessageContentT,
        ToolDefinitionsT,
        ToolSelectionT,
        ChatPredictionT,
    ]:
        return self.map(params)
