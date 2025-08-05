
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools

from chatio.core.params import ApiToolsOptions
from chatio.core.config import ApiConfigFormat

from ._base import ApiFormatBase


# pylint: disable=too-few-public-methods
class ApiToolsFormatterBase[
    ToolDefinitionsT,
    ToolSchemaT,
    ToolChoiceT,
    ApiConfigFormatT: ApiConfigFormat,
](
    ApiFormatBase[ApiConfigFormatT],
    ABC,
):

    @abstractmethod
    def _tool_schema(self, tool: ToolSchema) -> ToolSchemaT:
        ...

    @abstractmethod
    def _tool_definitions(self, tools: list[ToolSchemaT]) -> ToolDefinitionsT:
        ...

    @abstractmethod
    def _tool_choice_null(self) -> ToolChoiceT:
        ...

    @abstractmethod
    def _tool_choice_none(self) -> ToolChoiceT:
        ...

    @abstractmethod
    def _tool_choice_auto(self) -> ToolChoiceT:
        ...

    @abstractmethod
    def _tool_choice_any(self) -> ToolChoiceT:
        ...

    @abstractmethod
    def _tool_choice_name(self, tool_name: str) -> ToolChoiceT:
        ...

    def _tool_choice(self, tool_choice: ToolChoice | None) -> ToolChoiceT:

        if tool_choice is None:
            return self._tool_choice_null()

        if not tool_choice.mode and not tool_choice.name:
            return self._tool_choice_null()

        if not tool_choice.name:
            match tool_choice.mode:
                case 'none':
                    return self._tool_choice_none()
                case 'auto':
                    return self._tool_choice_auto()
                case 'any':
                    return self._tool_choice_any()
                case _:
                    raise ValueError
        else:
            match tool_choice.mode:
                case 'name':
                    return self._tool_choice_name(tool_choice.name)
                case _:
                    raise ValueError

    def format(self, tools: ChatTools) -> ApiToolsOptions[
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        _tool_defs = [self._tool_schema(tool) for tool in tools.tools]

        _tools = self._tool_definitions(_tool_defs)

        _tool_choice = self._tool_choice(tools.tool_choice)

        return ApiToolsOptions(_tools, _tool_choice)


# pylint: disable=too-few-public-methods
class ApiToolsFormatter[
    ToolDefinitionsT,
    ToolChoiceT,
](Protocol):

    @abstractmethod
    def format(self, tools: ChatTools) -> ApiToolsOptions[
        ToolDefinitionsT,
        ToolChoiceT,
    ]:
        ...
