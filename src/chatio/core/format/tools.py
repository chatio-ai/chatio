
from abc import ABC, abstractmethod

from chatio.core.models import ToolSchema
from chatio.core.models import ChatTools

from chatio.core.params import ApiToolsOptions


# pylint: disable=too-few-public-methods
class ApiToolsFormat[
    ToolsT,
    ToolSchemaT,
    ToolChoiceT,
](ABC):

    @abstractmethod
    def _tool_schema(self, schema: ToolSchema) -> ToolSchemaT:
        ...

    @abstractmethod
    def _tools(self, *schemas: ToolSchemaT) -> ToolsT:
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
    def _tool_choice_name(self, name: str) -> ToolChoiceT:
        ...

    def _tool_choice(self, mode: str | None, name: str | None) -> ToolChoiceT:
        if not mode and not name:
            return self._tool_choice_null()

        if not name:
            match mode:
                case 'none':
                    return self._tool_choice_none()
                case 'auto':
                    return self._tool_choice_auto()
                case 'any':
                    return self._tool_choice_any()
                case _:
                    raise ValueError
        else:
            match mode:
                case 'name' | None:
                    return self._tool_choice_name(name)
                case _:
                    raise ValueError

    def __call__(self, tools: ChatTools) -> ApiToolsOptions[ToolsT, ToolChoiceT]:
        return ApiToolsOptions(
            tools=self._tools(*(self._tool_schema(tool) for tool in tools.schemas)),
            tool_choice=self._tool_choice(tools.choice.mode, tools.choice.name),
        )
