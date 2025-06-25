
from collections.abc import Callable

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
class ApiParamsBase[
    SystemContent,
    MessageContent,
    ToolDefinitions,
    ToolSelection,
    ChatPrediction,
]:
    system: SystemContent | None = None
    messages: list[MessageContent] = field(default_factory=list)
    predict: ChatPrediction | None = None
    tools: ToolDefinitions | None = None
    tool_choice: ToolSelection | None = None


@dataclass
class ApiParams(ApiParamsBase[
    SystemMessage,
    ContentEntry,
    list[ToolSchema],
    ToolChoice,
    PredictMessage,
]):
    funcs: dict[str, Callable] = field(default_factory=dict)
