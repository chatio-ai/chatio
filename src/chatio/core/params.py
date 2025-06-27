
from dataclasses import dataclass, field

from typing import TypedDict


class ApiParamsOptions(TypedDict):
    pass


@dataclass
class ApiParamsGeneric[
    SystemContentT,
    MessageContentT,
    ToolDefinitionsT,
    ToolSelectionT,
    ApiParamsOptionsT: ApiParamsOptions,
]:
    system: SystemContentT | None = None
    messages: list[MessageContentT] = field(default_factory=list)
    options: ApiParamsOptionsT | None = None
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolSelectionT | None = None


@dataclass
class ApiParams:
    pass
