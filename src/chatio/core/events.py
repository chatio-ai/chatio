
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
class TextEvent(ChatEvent):
    text: str
    label: str | None = None


@dataclass
class DoneEvent(ChatEvent):
    text: str
