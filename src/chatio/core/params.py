
from dataclasses import dataclass


@dataclass
class ApiToolsOptions[
    ToolsT,
    ToolChoiceT,
]:
    tools: ToolsT
    tool_choice: ToolChoiceT
