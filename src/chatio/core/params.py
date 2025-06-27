
from dataclasses import dataclass, field

from typing import TypedDict


class ApiExtras(TypedDict):
    pass


@dataclass
class ApiParams[
    SystemContentT,
    MessageContentT,
    ToolDefinitionsT,
    ToolSelectionT,
    ApiExtrasT: ApiExtras,
]:
    system: SystemContentT | None = None
    messages: list[MessageContentT] = field(default_factory=list)
    extras: ApiExtrasT | None = None
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolSelectionT | None = None
