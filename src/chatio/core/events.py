
from dataclasses import dataclass


@dataclass
class ChatEvent:
    pass


@dataclass
class StatEvent(ChatEvent):
    input_tokens: int
    output_tokens: int
    cache_written: int
    cache_read: int
    predict_accepted: int
    predict_rejected: int


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
