
from abc import ABC, abstractmethod

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.config import ApiConfig


class ApiFormatTools[
    ToolDefinitionT,
    ToolDefinitionsT,
    ToolSelectionT,
    ApiConfigT: ApiConfig,
](ABC):

    def __init__(self, config: ApiConfigT) -> None:
        self._config = config

    @abstractmethod
    def tool_definition(self, name: str, desc: str, schema: dict) -> ToolDefinitionT:
        ...

    @abstractmethod
    def tool_definitions(self, tools: list[ToolDefinitionT]) -> ToolDefinitionsT | None:
        ...

    @abstractmethod
    def tool_selection_none(self) -> ToolSelectionT | None:
        ...

    @abstractmethod
    def tool_selection_auto(self) -> ToolSelectionT | None:
        ...

    @abstractmethod
    def tool_selection_any(self) -> ToolSelectionT | None:
        ...

    @abstractmethod
    def tool_selection_name(self, tool_name: str) -> ToolSelectionT | None:
        ...

    def tool_selection(self, tool_choice_mode: str | None, tool_choice_name: str | None,
                       tools: list[str]) -> ToolSelectionT | None:
        if not tool_choice_mode and not tool_choice_name:
            return None

        if not tools:
            raise ValueError

        if not tool_choice_name:
            match tool_choice_mode:
                case 'none':
                    return self.tool_selection_none()
                case 'auto':
                    return self.tool_selection_auto()
                case 'any':
                    return self.tool_selection_any()
                case _:
                    raise ValueError
        else:
            if tool_choice_name not in tools:
                raise ValueError

            match tool_choice_mode:
                case 'name':
                    return self.tool_selection_name(tool_choice_name)
                case _:
                    raise ValueError

    def tools(self, tools: list[ToolSchema] | None) -> ToolDefinitionsT | None:
        if tools is None:
            return None

        _tools = [self.tool_definition(tool.name, tool.desc, tool.schema) for tool in tools]

        return self.tool_definitions(_tools)

    def tool_choice(self, tool_choice: ToolChoice | None) -> ToolSelectionT | None:
        if tool_choice is None:
            return None

        return self.tool_selection(tool_choice.mode, tool_choice.name, tool_choice.tools)
