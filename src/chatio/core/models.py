
from dataclasses import dataclass, field


@dataclass
class MessageContent:
    pass


@dataclass
class CallRequest(MessageContent):
    tool_call_id: str
    tool_name: str
    tool_input: object


@dataclass
class CallResponse(MessageContent):
    tool_call_id: str
    tool_name: str
    tool_output: str


@dataclass
class TextMessage(MessageContent):
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
class PredictionMessage(TextMessage):
    pass


@dataclass
class ImageDocument(MessageContent):
    blob: bytes
    mimetype: str


@dataclass
class TextDocument(MessageContent):
    text: str
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


@dataclass
class ChatStateOptions:
    system: SystemMessage | None = None
    prediction: PredictionMessage | None = None


@dataclass
class ChatState:
    messages: list[MessageContent] = field(default_factory=list)
    options: ChatStateOptions = field(default_factory=ChatStateOptions)


@dataclass
class ChatTools:
    tools: list[ToolSchema] | None = None
    tool_choice: ToolChoice | None = None
