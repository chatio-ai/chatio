
from dataclasses import dataclass


@dataclass
class ApiStateOptions:
    pass


@dataclass
class ApiToolsOptions[
    ToolDefinitionsT,
    ToolChoiceT,
]:
    tools: ToolDefinitionsT
    tool_choice: ToolChoiceT


@dataclass
class ApiParams[
    ChatMessageT,
    ApiStateOptionsT: ApiStateOptions,
    ToolDefinitionsT,
    ToolChoiceT,
]:
    options: ApiStateOptionsT
    messages: list[ChatMessageT]
    tools: ApiToolsOptions[
        ToolDefinitionsT,
        ToolChoiceT,
    ]
