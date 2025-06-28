
from dataclasses import dataclass


@dataclass
class ApiStateOptions:
    pass


@dataclass
class ApiParamValues[
    MessageContentT,
    ToolDefinitionsT,
    ToolChoiceT,
    ApiStateOptionsT: ApiStateOptions,
]:
    options: ApiStateOptionsT
    messages: list[MessageContentT]
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolChoiceT | None = None


@dataclass
class ApiParams:
    pass
