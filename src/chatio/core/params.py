
from dataclasses import dataclass


@dataclass
class ApiStateOptions:
    pass


@dataclass
class ApiToolsOptions[
    ToolsT,
    ToolChoiceT,
]:
    tools: ToolsT
    tool_choice: ToolChoiceT


@dataclass
class ApiParams:
    pass


@dataclass
class ApiParamsImpl[
    ChatMessageT,
    ApiStateOptionsT: ApiStateOptions,
    ToolsT,
    ToolChoiceT,
](ApiParams):
    options: ApiStateOptionsT
    messages: list[ChatMessageT]
    tools: ApiToolsOptions[
        ToolsT,
        ToolChoiceT,
    ]
