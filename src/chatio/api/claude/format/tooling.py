
from typing import override

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.format.tooling import ApiFormatTooling

from chatio.api.claude.config import ClaudeConfig


class ClaudeFormatTooling(ApiFormatTooling[
    list[ToolParam] | NotGiven,
    ToolParam,
    ToolChoiceParam | NotGiven,
    ClaudeConfig,
]):

    def _setup_tools_cache(self, entries: list[ToolParam]) -> list[ToolParam]:
        if self._config.options.use_cache and entries:
            entry = entries[-1]

            entry.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return entries

    @override
    def tool_schema(self, name: str, desc: str, params: dict) -> ToolParam:
        return {
            "name": name,
            "description": desc,
            "input_schema": params,
        }

    @override
    def tool_definitions(self, tools: list[ToolParam] | None) -> list[ToolParam] | NotGiven:
        if tools is None:
            return NOT_GIVEN
        return self._setup_tools_cache(tools)

    def tool_choice_null(self) -> NotGiven:
        return NOT_GIVEN

    @override
    def tool_choice_none(self) -> ToolChoiceParam:
        return {
            "type": 'none',
        }

    @override
    def tool_choice_auto(self) -> ToolChoiceParam:
        return {
            "type": 'auto',
        }

    @override
    def tool_choice_any(self) -> ToolChoiceParam:
        return {
            "type": 'any',
        }

    @override
    def tool_choice_name(self, tool_name: str) -> ToolChoiceParam:
        return {
            "type": 'tool',
            "name": tool_name,
        }
