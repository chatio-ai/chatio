
from dataclasses import dataclass


@dataclass
class ApiParamsOptions:
    pass


@dataclass
class ApiParamsGeneric[
    MessageContentT,
    ToolDefinitionsT,
    ToolChoiceT,
    ApiParamsOptionsT: ApiParamsOptions,
]:
    options: ApiParamsOptionsT
    messages: list[MessageContentT]
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolChoiceT | None = None


@dataclass
class ApiParams:
    pass
