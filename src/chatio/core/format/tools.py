
from abc import ABC, abstractmethod

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools

from chatio.core.params import ApiToolsOptions


# pylint: disable=too-few-public-methods
class ApiToolsFormat[
    ToolsT,
    ToolSchemaT,
    ToolChoiceT,
](ABC):

    @abstractmethod
    def _tool_schema(self, tool: ToolSchema) -> ToolSchemaT:
        ...

    @abstractmethod
    def _tools(self, *tools: ToolSchemaT) -> ToolsT:
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

    def _tool_choice(self, tool_choice: ToolChoice) -> ToolChoiceT:
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
                case 'name' | None:
                    return self._tool_choice_name(tool_choice.name)
                case _:
                    raise ValueError

    def __call__(self, tools: ChatTools) -> ApiToolsOptions[ToolsT, ToolChoiceT]:
        return ApiToolsOptions(
            tools=self._tools(*(self._tool_schema(tool) for tool in tools.tools)),
            tool_choice=self._tool_choice(tools.tool_choice),
        )
