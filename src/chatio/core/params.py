
from collections.abc import Callable

from dataclasses import dataclass


@dataclass
class ApiParams[
    SystemContent,
    MessageContent,
    PredictionContent,
    ToolDefinitions,
    ToolSelection,
]:
    system: SystemContent | None
    messages: list[MessageContent]
    prediction: PredictionContent | None
    tools: ToolDefinitions | None
    funcs: dict[str, Callable]
    tool_choice: ToolSelection | None

    def __init__(self):
        self.system = None
        self.messages = []
        self.prediction = None
        self.tools = None
        self.funcs = {}
        self.tool_choice = None
