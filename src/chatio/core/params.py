
from abc import ABC, abstractmethod

from collections.abc import Callable

from dataclasses import dataclass

from chatio.core.format import ApiFormat


@dataclass
class ApiParams[
    SystemContent,
    MessageContent,
    PredictionContent,
    TextMessage,
    ImageMessage,
    ToolDefinition,
    ToolDefinitions,
    ToolSelection,
](ABC):

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

    @property
    @abstractmethod
    def format(self) -> ApiFormat[
        SystemContent,
        MessageContent,
        PredictionContent,
        TextMessage,
        ImageMessage,
        ToolDefinition,
        ToolDefinitions,
        ToolSelection,
    ]:
        ...
