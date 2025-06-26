
from typing import override

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam

from chatio.core.format.tools import ApiFormatTools

from chatio.api.claude.config import ClaudeConfig


class ClaudeFormatTools(ApiFormatTools[
    ToolParam,
    list[ToolParam],
    ToolChoiceParam,
]):

    def __init__(self, config: ClaudeConfig) -> None:
        self._config = config

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
    def tool_definition(self, name: str, desc: str, schema: dict) -> ToolParam:
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    @override
    def tool_definitions(self, tools: list[ToolParam]) -> list[ToolParam]:
        return self._setup_tools_cache(tools)

    @override
    def tool_selection_none(self) -> ToolChoiceParam | None:
        return {
            "type": 'none',
        }

    @override
    def tool_selection_auto(self) -> ToolChoiceParam | None:
        return {
            "type": 'auto',
        }

    @override
    def tool_selection_any(self) -> ToolChoiceParam | None:
        return {
            "type": 'any',
        }

    @override
    def tool_selection_name(self, tool_name: str) -> ToolChoiceParam | None:
        return {
            "type": 'tool',
            "name": tool_name,
        }
