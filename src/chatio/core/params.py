
from dataclasses import dataclass, field


@dataclass
class ApiParams[
    SystemContentT,
    MessageContentT,
    ChatPredictionT,
    ToolDefinitionsT,
    ToolSelectionT,
]:
    system: SystemContentT | None = None
    messages: list[MessageContentT] = field(default_factory=list)
    predict: ChatPredictionT | None = None
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolSelectionT | None = None
