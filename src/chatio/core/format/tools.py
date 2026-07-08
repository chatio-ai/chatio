
from abc import ABC, abstractmethod

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice


# pylint: disable=too-few-public-methods
class ApiToolSchemasFormat[
    ToolsT,
    ToolSchemaT,
](ABC):

    @abstractmethod
    def _tool_schema(self, schema: ToolSchema) -> ToolSchemaT:
        ...

    @abstractmethod
    def _tools(self, *schemas: ToolSchemaT) -> ToolsT:
        ...

    def __call__(self, schemas: list[ToolSchema]) -> ToolsT:
        return self._tools(*(self._tool_schema(tool) for tool in schemas))


# pylint: disable=too-few-public-methods
class ApiToolChoiceFormat[
    ToolChoiceT,
](ABC):

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

    def __call__(self, choice: ToolChoice) -> ToolChoiceT:
        return self._tool_choice(choice.mode, choice.name)
