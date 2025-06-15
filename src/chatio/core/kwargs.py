
from dataclasses import dataclass


@dataclass
class ChatKwargs[
    SystemContent,
    MessageContent,
    ToolDefinitions,
]:
    system: SystemContent | None
    messages: list[MessageContent]
    tools: ToolDefinitions | None
