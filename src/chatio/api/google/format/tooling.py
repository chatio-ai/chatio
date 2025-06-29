
from typing import override
from typing import TypeGuard

from google.genai.types import SchemaDict
from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionCallingConfigMode
from google.genai.types import FunctionDeclarationDict

from chatio.core.format.tooling import ApiFormatTooling

from chatio.api.google.config import GoogleConfig


class GoogleFormatTooling(ApiFormatTooling[
    ToolListUnionDict | None,
    FunctionDeclarationDict,
    ToolConfigDict | None,
    GoogleConfig,
]):

    def _is_tool_params_schema(self, _params: dict) -> TypeGuard[SchemaDict]:
        return True

    @override
    def tool_schema(self, name: str, desc: str, params: dict) -> FunctionDeclarationDict:
        if not self._is_tool_params_schema(params):
            raise TypeError

        return {
            "name": name,
            "description": desc,
            "parameters": params,
        }

    @override
    def tool_definitions(
        self, tools: list[FunctionDeclarationDict] | None,
    ) -> ToolListUnionDict | None:

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
    def tool_choice_null(self) -> None:
        return None

    @override
    def tool_choice_none(self) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.NONE,
            },
        }

    @override
    def tool_choice_auto(self) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.AUTO,
            },
        }

    @override
    def tool_choice_any(self) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
            },
        }

    @override
    def tool_choice_name(self, tool_name: str) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
                "allowed_function_names": [tool_name],
            },
        }
