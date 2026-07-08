
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

from chatio.core.format.tools import ApiToolSchemasFormat
from chatio.core.format.tools import ApiToolChoiceFormat


# pylint: disable=too-few-public-methods
class GoogleToolSchemasFormat(ApiToolSchemasFormat[
    ToolListUnionDict | None,
    FunctionDeclarationDict,
]):

    def __init__(self, *, grounding: bool) -> None:
        self._grounding = grounding

    def _is_tool_params_schema(self, _params: Mapping[str, Any]) -> TypeGuard[SchemaDict]:
        return True

    @override
    def _tool_schema(self, schema: ToolSchema) -> FunctionDeclarationDict:
        if not self._is_tool_params_schema(schema.params):
            raise TypeError

        return {
            "name": schema.name,
            "description": schema.desc,
            "parameters": schema.params,
        }

    @override
    def _tools(self, *schemas: FunctionDeclarationDict) -> ToolListUnionDict | None:
        result: ToolListUnionDict = []

        if schemas:
            result.append({
                "function_declarations": list(schemas),
            })

        if self._grounding:
            result.append({
                "google_search": {},
            })

        if not result:
            return None

        return result


# pylint: disable=too-few-public-methods
class GoogleToolChoiceFormat(ApiToolChoiceFormat[
    ToolConfigDict | None,
]):

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
    def _tool_choice_name(self, name: str) -> ToolConfigDict:
        return {
            "function_calling_config": {
                "mode": FunctionCallingConfigMode.ANY,
                "allowed_function_names": [name],
            },
        }
