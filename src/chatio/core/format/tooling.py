
from abc import ABC, abstractmethod

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.config import ApiConfig

from ._common import ApiFormatBase


class ApiFormatTooling[
    ToolDefinitionsT,
    ToolSchemaT,
    ToolChoiceT,
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
    ABC,
):

    @abstractmethod
    def tool_schema(self, name: str, desc: str, params: dict) -> ToolSchemaT:
        ...

    @abstractmethod
    def tool_definitions(self, tools: list[ToolSchemaT]) -> ToolDefinitionsT | None:
        ...

    @abstractmethod
    def tool_choice_none(self) -> ToolChoiceT | None:
        ...

    @abstractmethod
    def tool_choice_auto(self) -> ToolChoiceT | None:
        ...

    @abstractmethod
    def tool_choice_any(self) -> ToolChoiceT | None:
        ...

    @abstractmethod
    def tool_choice_name(self, tool_name: str) -> ToolChoiceT | None:
        ...

    def _tool_choice(
        self, tool_choice_mode: str | None, tool_choice_name: str | None, tools: list[str],
    ) -> ToolChoiceT | None:

        if not tool_choice_mode and not tool_choice_name:
            return None

        if not tools:
            raise ValueError

        if not tool_choice_name:
            match tool_choice_mode:
                case 'none':
                    return self.tool_choice_none()
                case 'auto':
                    return self.tool_choice_auto()
                case 'any':
                    return self.tool_choice_any()
                case _:
                    raise ValueError
        else:
            if tool_choice_name not in tools:
                raise ValueError

            match tool_choice_mode:
                case 'name':
                    return self.tool_choice_name(tool_choice_name)
                case _:
                    raise ValueError

    def tools(self, tools: list[ToolSchema] | None) -> ToolDefinitionsT | None:
        if tools is None:
            return None

        _tools = [self.tool_schema(tool.name, tool.desc, tool.schema) for tool in tools]

        return self.tool_definitions(_tools)

    def tool_choice(self, tool_choice: ToolChoice | None) -> ToolChoiceT | None:
        if tool_choice is None:
            return None

        return self._tool_choice(tool_choice.mode, tool_choice.name, tool_choice.tools)
