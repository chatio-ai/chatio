
from typing import override

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven, NOT_GIVEN

from chatio.core.models import ToolSchema

from chatio.core.format.tools import ApiToolsFormatterBase

from chatio.api.claude.config import ClaudeConfigFormat


# pylint: disable=too-few-public-methods
class ClaudeToolsFormatter(ApiToolsFormatterBase[
    list[ToolParam] | NotGiven,
    ToolParam,
    ToolChoiceParam | NotGiven,
    ClaudeConfigFormat,
]):

    def _setup_tools_cache(self, entries: list[ToolParam]) -> list[ToolParam]:
        if self._config.use_cache and entries:
            entry = entries[-1]

            entry.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return entries

    @override
    def _tool_schema(self, tool: ToolSchema) -> ToolParam:
        return {
            "name": tool.name,
            "description": tool.desc,
            "input_schema": tool.params,
        }

    @override
    def _tool_definitions(self, tools: list[ToolParam] | None) -> list[ToolParam] | NotGiven:
        if tools is None:
            return NOT_GIVEN
        return self._setup_tools_cache(tools)

    def _tool_choice_null(self) -> NotGiven:
        return NOT_GIVEN

    @override
    def _tool_choice_none(self) -> ToolChoiceParam:
        return {
            "type": 'none',
        }

    @override
    def _tool_choice_auto(self) -> ToolChoiceParam:
        return {
            "type": 'auto',
        }

    @override
    def _tool_choice_any(self) -> ToolChoiceParam:
        return {
            "type": 'any',
        }

    @override
    def _tool_choice_name(self, tool_name: str) -> ToolChoiceParam:
        return {
            "type": 'tool',
            "name": tool_name,
        }
