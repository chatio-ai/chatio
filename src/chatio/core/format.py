
from abc import ABC, abstractmethod

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

from .models import ChatState
from .models import ChatTools

from .params import ApiParams


class ApiHelper[
    SystemContentT,
    MessageContentT,
    ChatPredictionT,
    TextMessageT,
    ImageDocumentT,
    TextDocumentT,
    ToolDefinitionT,
    ToolDefinitionsT,
    ToolSelectionT,
](ABC):

    # messages

    @abstractmethod
    def chat_messages(self, messages: list[MessageContentT]) -> list[MessageContentT]:
        ...

    @abstractmethod
    def text_message(self, text: str) -> TextMessageT:
        ...

    @abstractmethod
    def text_document_chunk(self, text: str, mimetype: str) -> TextDocumentT:
        ...

    @abstractmethod
    def image_document_blob(self, blob: bytes, mimetype: str) -> ImageDocumentT:
        ...

    @abstractmethod
    def system_content(self, content: TextMessageT) -> SystemContentT:
        ...

    @abstractmethod
    def prediction_content(self, content: TextMessageT) -> ChatPredictionT | None:
        ...

    @abstractmethod
    def input_content(self, content: TextMessageT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def input_message(self, message: str) -> MessageContentT:
        return self.input_content(self.text_message(message))

    @abstractmethod
    def output_content(self, content: TextMessageT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def output_message(self, message: str) -> MessageContentT:
        return self.output_content(self.text_message(message))

    @abstractmethod
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> MessageContentT:
        ...

    @abstractmethod
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> MessageContentT:
        ...

    def image_document(self, blob: bytes, mimetype: str) -> MessageContentT:
        return self.input_content(self.image_document_blob(blob, mimetype))

    def text_document(self, text: str, mimetype: str) -> MessageContentT:
        return self.input_content(self.text_document_chunk(text, mimetype))

    # functions

    @abstractmethod
    def tool_definition(self, name: str, desc: str, schema: dict) -> ToolDefinitionT:
        ...

    @abstractmethod
    def tool_definitions(self, tools: list[ToolDefinitionT]) -> ToolDefinitionsT | None:
        ...

    @abstractmethod
    def tool_selection_none(self) -> ToolSelectionT | None:
        ...

    @abstractmethod
    def tool_selection_auto(self) -> ToolSelectionT | None:
        ...

    @abstractmethod
    def tool_selection_any(self) -> ToolSelectionT | None:
        ...

    # @abstractmethod
    # def tool_selection_name(self, tool_name: str) -> ToolSelectionT | None:
    #     ...

    def tool_selection(self, tool_choice_mode: str | None, tool_choice_name: str | None,
                       tools: list[str]) -> ToolSelectionT | None:
        if not tool_choice_mode and not tool_choice_name:
            return None

        if not tools:
            raise ValueError

        if not tool_choice_name:
            match tool_choice_mode:
                case 'none':
                    return self.tool_selection_none()
                case 'auto':
                    return self.tool_selection_auto()
                case 'any':
                    return self.tool_selection_any()
                case _:
                    raise ValueError
        else:
            if tool_choice_name not in tools:
                raise ValueError

            match tool_choice_mode:
                case 'name':
                    # return self.tool_selection_name(tool_choice_name)
                    raise NotImplementedError
                case _:
                    raise ValueError


class ApiFormat[
    SystemContentT,
    MessageContentT,
    ChatPredictionT,
    TextMessageT,
    ImageDocumentT,
    TextDocumentT,
    ToolDefinitionT,
    ToolDefinitionsT,
    ToolSelectionT,
](ABC):

    def __init__(self, helper: ApiHelper):
        self._helper = helper

    def _system(self, message: SystemMessage | None) -> SystemContentT | None:
        if message is None:
            return None

        return self._helper.system_content(self._helper.text_message(message.text))

    def _messages(self, messages: list[ContentEntry]) -> list[MessageContentT]:
        _messages = []

        for message in messages:
            match message:
                case InputMessage(text):
                    _messages.append(self._helper.input_message(text))
                case OutputMessage(text):
                    _messages.append(self._helper.output_message(text))
                case CallRequest(tool_call_id, tool_name, tool_input):
                    _messages.append(self._helper.call_request(tool_call_id, tool_name, tool_input))
                case CallResponse(tool_call_id, tool_name, tool_output):
                    _messages.append(self._helper.call_response(tool_call_id, tool_name, tool_output))
                case TextDocument(text, mimetype):
                    _messages.append(self._helper.text_document(text, mimetype))
                case ImageDocument(blob, mimetype):
                    _messages.append(self._helper.image_document(blob, mimetype))
                case _:
                    raise RuntimeError(message)

        return self._helper.chat_messages(_messages)

    def _tool_specs(self, tools: list[ToolSchema] | None) -> ToolDefinitionsT | None:
        if tools is None:
            return None

        _tools = [self._helper.tool_definition(tool.name, tool.desc, tool.schema) for tool in tools]

        return self._helper.tool_definitions(_tools)

    def _tool_choice(self, tool_choice: ToolChoice | None) -> ToolSelectionT | None:
        if tool_choice is None:
            return None

        return self._helper.tool_selection(tool_choice.mode, tool_choice.name, tool_choice.tools)

    def _predict(self, message: PredictMessage | None) -> ChatPredictionT | None:
        if message is None:
            return None

        return self._helper.prediction_content(self._helper.text_message(message.text))

    def setup(self, params: ApiParams[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ], state: ChatState, tools: ChatTools):
        # _predict = state.extras.get('prediction')
        # if _predict is not None and not isinstance(_predict, PredictMessage):
        #     raise TypeError(_predict)

        params.system = self._system(state.system)
        params.messages = self._messages(state.messages)
        # params.predict = self._predict(_predict)
        params.tools = self._tool_specs(tools.tools)
        params.tool_choice = self._tool_choice(tools.tool_choice)

    @abstractmethod
    def spawn(self) -> ApiParams[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ]:
        pass

    @abstractmethod
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ]:
        ...
