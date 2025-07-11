
from dataclasses import dataclass


@dataclass
class ChatEvent:
    pass


@dataclass
class StatEvent(ChatEvent):
    label: str
    delta: int
    total: int | None = None


@dataclass
class CallEvent(ChatEvent):
    call_id: str
    name: str
    args: dict
    args_raw: object


@dataclass
class ToolEvent(ChatEvent):
    call_id: str
    name: str
    data: dict


@dataclass
class TextChunk(ChatEvent):
    text: str
    label: str | None = None


@dataclass
class ModelTextChunk(TextChunk):
    pass


@dataclass
class ToolsTextChunk(TextChunk):
    pass


@dataclass
class StopEvent(ChatEvent):
    text: str
