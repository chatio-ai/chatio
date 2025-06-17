
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
    tool_choice: ToolSelection | None
