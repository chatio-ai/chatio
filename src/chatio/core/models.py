
from dataclasses import dataclass


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
