
from typing import override

from chatio.api._common import ChatFormat

from .params import OpenAIParams


class OpenAIFormat(ChatFormat):

    def __init__(self, params: OpenAIParams):
        self._params = params

    # messages

    @override
    def chat_messages(self, messages: list[dict]) -> list[dict]:
        return messages

    @override
    def text_chunk(self, text: str) -> dict:
        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_blob(self, blob: str, mimetype: str) -> dict:
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mimetype};base64,{blob}"},
        }

    # messages

    def _as_contents_compat(self, content: list[dict] | dict | str) -> list[dict] | str:
        match content, self._params.legacy:
            case str(), True:
                return content
            case _:
                return self._as_contents(content)

    @override
    def system_message(self, content: str) -> tuple[list[dict], list[dict]]:
        if not content:
            return [], []

        return [], [{
            "role": "developer",
            "content": self._as_contents_compat(content),
        }]

    @override
    def input_message(self, content: str) -> dict:
        return {
            "role": "user",
            "content": self._as_contents_compat(content),
        }

    @override
    def output_message(self, content: str) -> dict:
        return {
            "role": "assistant",
            "content": self._as_contents_compat(content),
        }

    @override
    def tool_request(self, tool_call_id: str, tool_name: str, tool_input: dict) -> dict:
        return {
            "role": "assistant",
            "tool_calls": [{
                "id": tool_call_id,
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": tool_input,
                },
            }],
        }

    @override
    def tool_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> dict:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_output,
        }

    def predict_content(self, prediction: str) -> dict:
        return {
            "type": "content",
            "content": prediction,
        }

    # functions

    def _tool_schema(self, schema: dict) -> dict:
        result = schema.copy()

        props = None
        if result.get("type") == "object":
            props = result.setdefault("properties", {})

        if props is not None:
            result.update({
                "additionalProperties": False,
                "required": list(props),
            })

            for key in props:
                value = props.get(key, {})
                value = self._tool_schema(value)
                props[key] = value

        return result

    @override
    def tool_definition(self, name: str, desc: str, schema: dict) -> dict:
        schema = self._tool_schema(schema)
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": schema,
                "strict": True,
            },
        }

    @override
    def tool_definitions(self, tools: list[dict]) -> list[dict]:
        return tools

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
