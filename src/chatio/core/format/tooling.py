
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import ChatTools

from chatio.core.params import ApiToolsOptions
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

    def format(self, tools: ChatTools) -> ApiToolsOptions[
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        _tools = None
        if tools.tools is not None:
            _tool_defs = [self.tool_schema(tool.name, tool.desc, tool.schema) for tool in tools.tools]
            _tools = self.tool_definitions(_tool_defs)

        _tool_choice = None
        if tools.tool_choice is not None:
            _tool_choice = self._tool_choice(
                tools.tool_choice.mode, tools.tool_choice.name, tools.tool_choice.tools)

        return ApiToolsOptions(_tools, _tool_choice)


# pylint: disable=too-few-public-methods
class ApiFormatToolingProto[
    ToolDefinitionsT,
    ToolChoiceT,
](Protocol):

    @abstractmethod
    def format(self, tools: ChatTools) -> ApiToolsOptions[
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        ...
