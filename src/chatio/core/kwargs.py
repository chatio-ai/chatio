
from dataclasses import dataclass


@dataclass
class ChatKwargs[
    SystemContent,
    MessageContent,
    ToolDefinitions,
    ToolSelection,
]:
    system: SystemContent | None
    messages: list[MessageContent]
    tools: ToolDefinitions | None
    tool_choice: ToolSelection | None
