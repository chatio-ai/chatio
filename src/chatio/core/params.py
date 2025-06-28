
from dataclasses import dataclass


@dataclass
class ApiStateOptions:
    pass


@dataclass
class ApiToolsOptions[
    ToolDefinitionsT,
    ToolChoiceT,
]:
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolChoiceT | None = None


@dataclass
class ApiParamValues[
    MessageContentT,
    ApiStateOptionsT: ApiStateOptions,
    ApiToolsOptionsT: ApiToolsOptions,
]:
    options: ApiStateOptionsT
    messages: list[MessageContentT]
    tools: ApiToolsOptionsT


@dataclass
class ApiParams:
    pass
