
from collections.abc import Mapping

from typing import override
from typing import TypeGuard
from typing import Any

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic.types.tool_param import InputSchemaTyped

from anthropic import Omit, omit

from chatio.core.models import ToolSchema

from chatio.core.format.tools import ApiToolSchemasFormat
from chatio.core.format.tools import ApiToolChoiceFormat


# pylint: disable=too-few-public-methods
class ClaudeToolSchemasFormat(ApiToolSchemasFormat[
    list[ToolParam] | Omit,
    ToolParam,
]):

    def __init__(self, *, use_cache: bool) -> None:
        self._use_cache = use_cache

    def _setup_tools_cache(self, entries: list[ToolParam]) -> list[ToolParam]:
        if self._use_cache and entries:
            entry = entries[-1]

            entry.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return entries

    def _is_tool_params_schema(self, _params: Mapping[str, Any]) -> TypeGuard[InputSchemaTyped]:
        return True

    @override
    def _tool_schema(self, schema: ToolSchema) -> ToolParam:
        if not self._is_tool_params_schema(schema.params):
            raise TypeError

        return {
            "name": schema.name,
            "description": schema.desc,
            "input_schema": schema.params,
        }

    @override
    def _tools(self, *schemas: ToolParam) -> list[ToolParam] | Omit:
        if not schemas:
            return omit
        return self._setup_tools_cache(list(schemas))


class ClaudeToolChoiceFormat(ApiToolChoiceFormat[
    ToolChoiceParam | Omit,
]):

    @override
    def _tool_choice_null(self) -> Omit:
        return omit

    @override
    def _tool_choice_none(self) -> ToolChoiceParam:
        return {
            "type": "none",
        }

    @override
    def _tool_choice_auto(self) -> ToolChoiceParam:
        return {
            "type": "auto",
        }

    @override
    def _tool_choice_any(self) -> ToolChoiceParam:
        return {
            "type": "any",
        }

    @override
    def _tool_choice_name(self, name: str) -> ToolChoiceParam:
        return {
            "type": "tool",
            "name": name,
        }
