
from typing import override

from chatio.core.format import ChatFormat

from .params import GoogleParams


class GoogleFormat(ChatFormat):

    def __init__(self, params: GoogleParams):
        self._params = params

    # messages

    @override
    def chat_messages(self, messages: list[dict]) -> list[dict]:
        return messages

    @override
    def text_chunk(self, text: str) -> dict:
        return {
            "text": text,
        }

    @override
    def image_blob(self, blob: str, mimetype: str) -> dict:
        return {
            "inline_data": {
                "mime_type": mimetype,
                "data": blob,
            },
        }

    def _as_contents(self, content: dict) -> list[dict]:
        return [content]

    @override
    def system_content(self, content: dict) -> dict:
        return {
            "parts": self._as_contents(content),
        }

    @override
    def input_content(self, content: dict) -> dict:
        return {
            "role": "user",
            "parts": self._as_contents(content),
        }

    @override
    def output_content(self, content: dict) -> dict:
        return {
            "role": "model",
            "parts": self._as_contents(content),
        }

    @override
    def tool_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> dict:
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
    def tool_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> dict:
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

    @override
    def tool_definition(self, name: str, desc: str, schema: dict) -> dict:
        return {
            "name": name,
            "description": desc,
            "parameters": schema,
        }

    @override
    def tool_definitions(self, tools: list[dict]) -> list[dict] | None:
        tools_config: list[dict] = []

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
