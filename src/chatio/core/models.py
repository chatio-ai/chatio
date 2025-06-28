
from dataclasses import dataclass, field


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
class SystemContent(TextMessage):
    pass


@dataclass
class InputMessage(TextMessage):
    pass


@dataclass
class OutputMessage(TextMessage):
    pass


@dataclass
class PredictContent(TextMessage):
    pass


@dataclass
class ImageDocument(ContentEntry):
    blob: bytes
    mimetype: str


@dataclass
class TextDocument(ContentEntry):
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
    tools: list[str]


@dataclass
class StateOptions:
    system: SystemContent | None = None
    prediction: PredictContent | None = None


@dataclass
class ChatState:
    messages: list[ContentEntry] = field(default_factory=list)
    options: StateOptions = field(default_factory=StateOptions)


@dataclass
class ChatTools:
    tools: list[ToolSchema] | None = None
    tool_choice: ToolChoice | None = None
