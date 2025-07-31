
from collections.abc import Mapping

from dataclasses import dataclass, field

from typing import Any


@dataclass
class ChatMessage:
    pass


@dataclass
class CallRequest(ChatMessage):
    tool_call_id: str
    tool_name: str
    tool_input: object


@dataclass
class CallResponse(ChatMessage):
    tool_call_id: str
    tool_name: str
    tool_output: str


@dataclass
class TextMessage(ChatMessage):
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
class ImageDocument(ChatMessage):
    blob: bytes
    mimetype: str


@dataclass
class TextDocument(ChatMessage):
    text: str
    mimetype: str


@dataclass
class ToolSchema:
    name: str
    desc: str
    params: Mapping[str, Any]


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
    messages: list[ChatMessage] = field(default_factory=list)
    options: ChatStateOptions = field(default_factory=ChatStateOptions)


@dataclass
class ChatTools:
    tools: list[ToolSchema] | None = None
    tool_choice: ToolChoice | None = None
