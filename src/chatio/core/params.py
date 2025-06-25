
from collections.abc import Callable

from dataclasses import dataclass

from chatio.core.format import ApiFormat


@dataclass
class ContentEntry:
    pass


@dataclass
class CallRequest(ContentEntry):
    tool_call_id: str
    tool_name: str
    tool_input: object


@dataclass
class CallResponse(ContentEntry):
    tool_call_id: str
    tool_name: str
    tool_output: str


@dataclass
class TextMessage(ContentEntry):
    text: str


@dataclass
class SystemMessage(TextMessage):
    pass


@dataclass
class InputMessage(TextMessage):
    pass


@dataclass
class OutputMessage(TextMessage):
    pass


@dataclass
class PredictMessage(TextMessage):
    pass


@dataclass
class ImageDocument(ContentEntry):
    blob: bytes
    mimetype: str


@dataclass
class ToolSchema:
    name: str
    desc: str
    schema: dict


@dataclass
class ToolChoice:
    mode: str | None
    name: str | None
    tools: list[str]


@dataclass
class ApiStates:
    system: SystemMessage | None
    messages: list[ContentEntry]
    predict: PredictMessage | None
    funcs: dict[str, Callable]
    tools: list[ToolSchema] | None
    tool_choice: ToolChoice | None

    def __init__(self):
        self.system = None
        self.messages = []
        self.prediction = None
        self.funcs = {}
        self.tools = None
        self.tool_choice = None


@dataclass
class ApiParams[
    SystemContent,
    MessageContent,
    ToolDefinitions,
    ToolSelection,
    ChatPrediction,
]:
    system: SystemContent | None
    messages: list[MessageContent]
    predict: ChatPrediction | None
    tools: ToolDefinitions | None
    tool_choice: ToolSelection | None


class ApiMapper[
    SystemContent,
    MessageContent,
    ChatPrediction,
    TextMessage,
    ImageMessage,
    ToolDefinition,
    ToolDefinitions,
    ToolSelection,
]:

    def __init__(self, formatter: ApiFormat[
        SystemContent,
        MessageContent,
        ChatPrediction,
        TextMessage,
        ImageMessage,
        ToolDefinition,
        ToolDefinitions,
        ToolSelection,
    ]):
        self._format = formatter

    def system(self, message: SystemMessage | None) -> SystemContent | None:
        if message is None:
            return None

        return self._format.system_content(self._format.text_chunk(message.text))

    def messages(self, messages: list[ContentEntry]) -> list[MessageContent]:
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
                case ImageDocument(blob, mimetype):
                    _messages.append(self._format.image_document(blob, mimetype))
                case _:
                    raise RuntimeError(message)

        return self._format.chat_messages(_messages)

    def tools(self, tools: list[ToolSchema] | None) -> ToolDefinitions | None:
        if tools is None:
            return None

        _tools = [self._format.tool_definition(tool.name, tool.desc, tool.schema) for tool in tools]

        return self._format.tool_definitions(_tools)

    def tool_choice(self, tool_choice: ToolChoice | None) -> ToolSelection | None:
        if tool_choice is None:
            return None

        return self._format.tool_selection(tool_choice.mode, tool_choice.name, tool_choice.tools)

    def predict(self, message: PredictMessage | None) -> ChatPrediction | None:
        if message is None:
            return None

        return self._format.prediction_content(self._format.text_chunk(message.text))

    def map(self, states: ApiStates) -> ApiParams[
        SystemContent,
        MessageContent,
        ToolDefinitions,
        ToolSelection,
        ChatPrediction,
    ]:
        return ApiParams(
            system=self.system(states.system),
            messages=self.messages(states.messages),
            predict=self.predict(states.predict),
            tools=self.tools(states.tools),
            tool_choice=self.tool_choice(states.tool_choice),
        )
