
from dataclasses import dataclass


@dataclass
class StatEvent:
    input_tokens: int
    output_tokens: int
    cache_written: int
    cache_read: int
    predict_accepted: int
    predict_rejected: int


@dataclass
class CallEvent:
    call_id: str
    name: str
    args: dict
    input: str


@dataclass
class TextEvent:
    text: str
    label: str | None = None


@dataclass
class DoneEvent:
    text: str
