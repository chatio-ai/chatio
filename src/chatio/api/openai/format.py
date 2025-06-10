
from typing import override

from chatio.api._common import ChatFormat

from .params import OpenAIParams


class OpenAIFormat(ChatFormat):

    def __init__(self, params: OpenAIParams):
        self._params = params

    # messages

    @override
    def chat_messages(self, messages):
        return messages

    @override
    def text_chunk(self, text):
        if self._params.legacy:
            return text

        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_blob(self, blob, mimetype):
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mimetype};base64,{blob}"},
        }

    @override
    def system_message(self, content):
        if not content:
            return [], []

        return [], [{
            "role": "developer",
            "content": self._as_contents(content),
        }]

    @override
    def input_message(self, content):
        return {
            "role": "user",
            "content": self._as_contents(content),
        }

    @override
    def output_message(self, content):
        return {
            "role": "assistant",
            "content": self._as_contents(content),
        }

    @override
    def tool_request(self, tool_call_id, tool_name, tool_input):
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
    def tool_response(self, tool_call_id, tool_name, tool_output):
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_output,
        }

    def predict_content(self, prediction):
        return {
            "type": "content",
            "content": prediction,
        }

    # functions

    def _tool_schema(self, schema):
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
    def tool_definition(self, name, desc, schema):
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
    def tool_definitions(self, tools):
        return tools

    @override
    def tool_selection(self, tool_choice, tool_choice_name):
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
