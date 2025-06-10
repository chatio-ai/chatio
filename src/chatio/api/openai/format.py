
from typing import override

from chatio.core.format import ChatFormat

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

    def _as_contents(self, content: dict) -> list[dict] | str:
        match content['type'], self._params.legacy:
            case 'text', True:
                return content['text']
            case _:
                return [content]

    @override
    def system_message(self, message: str | None) -> tuple[list[dict], list[dict]]:
        if not message:
            return [], []

        return [], [{
            "role": "system" if self._params.legacy else "developer",
            "content": self._as_contents(self.text_chunk(message)),
        }]

    @override
    def input_content(self, content: dict) -> dict:
        return {
            "role": "user",
            "content": self._as_contents(content),
        }

    @override
    def output_content(self, content: dict) -> dict:
        return {
            "role": "assistant",
            "content": self._as_contents(content),
        }

    @override
    def tool_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> dict:
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
