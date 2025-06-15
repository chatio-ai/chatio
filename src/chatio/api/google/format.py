
from typing import override
from typing import TypeGuard

from google.genai.types import ContentDict
from google.genai.types import PartDict

from google.genai.types import SchemaDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionDeclarationDict


from chatio.core.format import ChatFormat

from .params import GoogleParams


class GoogleFormat(ChatFormat[
    ContentDict,
    ContentDict,
    PartDict,
    PartDict,
    FunctionDeclarationDict,
    ToolListUnionDict,
]):

    def __init__(self, params: GoogleParams):
        self._params = params

    # messages

    @override
    def chat_messages(self, messages: list[ContentDict]) -> list[ContentDict]:
        return messages

    @override
    def text_chunk(self, text: str) -> PartDict:
        return {
            "text": text,
        }

    @override
    def image_blob(self, blob: bytes, mimetype: str) -> PartDict:
        return {
            "inline_data": {
                "mime_type": mimetype,
                "data": blob,
            },
        }

    @override
    def system_content(self, content: PartDict) -> ContentDict:
        return {
            "parts": [content],
        }

    @override
    def input_content(self, content: PartDict) -> ContentDict:
        return {
            "role": "user",
            "parts": [content],
        }

    @override
    def output_content(self, content: PartDict) -> ContentDict:
        return {
            "role": "model",
            "parts": [content],
        }

    @override
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> ContentDict:
        if not isinstance(tool_input, dict):
            raise TypeError

        return {
            "role": "model",
            "parts": [{
                "function_call": {
                    "id": tool_call_id,
                    "name": tool_name,
                    "args": tool_input,
                },
            }],
        }

    @override
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> ContentDict:
        return {
            "role": "user",
            "parts": [{
                "function_response": {
                    "id": tool_call_id,
                    "name": tool_name,
                    "response": {
                        "output": tool_output,
                    },
                },
            }],
        }

    # functions

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

        if self._params.grounding:
            tools_config.append({
                "google_search": {},
            })

        if not tools_config:
            return None

        return tools_config

    @override
    def tool_selection(self, tool_choice: str | None, tool_choice_name: str | None) -> dict | None:
        if not tool_choice:
            return None

        if not tool_choice_name:
            return {
                "type": tool_choice,
            }

        return {
            "type": tool_choice,
            "function": {
                "name": tool_choice_name,
            },
        }
