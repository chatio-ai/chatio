
from typing import override
from typing import TypeGuard

from google.genai.types import SchemaDict
from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionCallingConfigMode
from google.genai.types import FunctionDeclarationDict

from chatio.core.format.tools import ApiFormatTools

from chatio.api.google.config import GoogleConfig


class GoogleFormatTools(ApiFormatTools[
    FunctionDeclarationDict,
    ToolListUnionDict,
    ToolConfigDict,
    GoogleConfig,
]):

    def _is_tool_schema(self, _schema: dict) -> TypeGuard[SchemaDict]:
        return True

    @override
    def tool_definition(self, name: str, desc: str, schema: dict) -> FunctionDeclarationDict:
        if not self._is_tool_schema(schema):
            raise TypeError

        return {
            "name": name,
            "description": desc,
            "parameters": schema,
        }

    @override
    def tool_definitions(self, tools: list[FunctionDeclarationDict]) -> ToolListUnionDict | None:
        tools_config: ToolListUnionDict = []

        if tools:
            tools_config.append({
                "function_declarations": tools,
            })

        if self._config.options.grounding:
            tools_config.append({
                "google_search": {},
            })

        if not tools_config:
            return None

        return tools_config

    @override
    def tool_selection_none(self) -> ToolConfigDict | None:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.NONE,
            },
        }

    @override
    def tool_selection_auto(self) -> ToolConfigDict | None:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.AUTO,
            },
        }

    @override
    def tool_selection_any(self) -> ToolConfigDict | None:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
            },
        }

    @override
    def tool_selection_name(self, tool_name: str) -> ToolConfigDict | None:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
                "allowed_function_names": [tool_name],
            },
        }
