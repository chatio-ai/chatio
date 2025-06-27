
from typing import override

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from chatio.core.format.tooling import ApiFormatTooling

from chatio.api.claude.config import ClaudeConfig


class ClaudeFormatTooling(ApiFormatTooling[
    list[ToolParam],
    ToolParam,
    ToolChoiceParam,
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
    def tool_definitions(self, tools: list[ToolParam]) -> list[ToolParam]:
        return self._setup_tools_cache(tools)

    @override
    def tool_choice_none(self) -> ToolChoiceParam | None:
        return {
            "type": 'none',
        }

    @override
    def tool_choice_auto(self) -> ToolChoiceParam | None:
        return {
            "type": 'auto',
        }

    @override
    def tool_choice_any(self) -> ToolChoiceParam | None:
        return {
            "type": 'any',
        }

    @override
    def tool_choice_name(self, tool_name: str) -> ToolChoiceParam | None:
        return {
            "type": 'tool',
            "name": tool_name,
        }
