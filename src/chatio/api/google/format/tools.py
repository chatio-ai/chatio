
from collections.abc import Mapping

from typing import override
from typing import TypeGuard
from typing import Any

from google.genai.types import SchemaDict
from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionCallingConfigMode
from google.genai.types import FunctionDeclarationDict

from chatio.core.models import ToolSchema

from chatio.core.format.tools import ApiToolsFormatterBase

from chatio.api.google.config import GoogleConfigFormat


# pylint: disable=too-few-public-methods
class GoogleToolsFormatter(ApiToolsFormatterBase[
    ToolListUnionDict | None,
    FunctionDeclarationDict,
    ToolConfigDict | None,
    GoogleConfigFormat,
]):

    def _is_tool_params_schema(self, _params: Mapping[str, Any]) -> TypeGuard[SchemaDict]:
        return True

    @override
    def _tool_schema(self, tool: ToolSchema) -> FunctionDeclarationDict:
        if not self._is_tool_params_schema(tool.params):
            raise TypeError

        return {
            "name": tool.name,
            "description": tool.desc,
            "parameters": tool.params,
        }

    @override
    def _tool_definitions(
        self, tools: list[FunctionDeclarationDict] | None,
    ) -> ToolListUnionDict | None:

        tools_config: ToolListUnionDict = []

        if tools:
            tools_config.append({
                "function_declarations": tools,
            })

        if self._config.grounding:
            tools_config.append({
                "google_search": {},
            })

        if not tools_config:
            return None

        return tools_config

    @override
    def _tool_choice_null(self) -> None:
        return None

    @override
    def _tool_choice_none(self) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.NONE,
            },
        }

    @override
    def _tool_choice_auto(self) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.AUTO,
            },
        }

    @override
    def _tool_choice_any(self) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
            },
        }

    @override
    def _tool_choice_name(self, tool_name: str) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
                "allowed_function_names": [tool_name],
            },
        }
