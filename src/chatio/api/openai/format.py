
import base64

from typing import override

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat import ChatCompletionPredictionContentParam
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam


from chatio.core.format import ApiFormat

from .config import OpenAIConfig


type _ChatCompletionContentPartParam = \
    ChatCompletionContentPartTextParam | ChatCompletionContentPartImageParam


class OpenAIFormat(ApiFormat[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionPredictionContentParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
]):

    def __init__(self, config: OpenAIConfig):
        self._config = config

    # messages

    @override
    def chat_messages(self, messages: list[ChatCompletionMessageParam]) -> list[ChatCompletionMessageParam]:
        return messages

    @override
    def text_chunk(self, text: str) -> ChatCompletionContentPartTextParam:
        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_blob(self, blob: bytes, mimetype: str) -> ChatCompletionContentPartImageParam:
        data = base64.b64encode(blob).decode('ascii')

        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mimetype};base64,{data}",
            },
        }

    @override
    def system_content(self, content: _ChatCompletionContentPartParam) -> ChatCompletionMessageParam:
        if content['type'] != 'text':
            raise TypeError

        if self._config.options.legacy:
            return {
                "role": "system",
                "content": content['text'],
            }

        return {
            "role": "developer",
            "content": [content],
        }

    @override
    def prediction_content(self,
                           content: ChatCompletionContentPartTextParam) -> ChatCompletionPredictionContentParam | None:
        if not self._config.options.prediction:
            return None

        return {
            "type": "content",
            "content": [content],
        }

    @override
    def input_content(self, content: _ChatCompletionContentPartParam) -> ChatCompletionMessageParam:
        if content['type'] != 'text':
            return {
                "role": "user",
                "content": [content],
            }

        return {
            "role": "user",
            "content": content['text'] if self._config.options.legacy else [content],
        }

    @override
    def output_content(self, content: _ChatCompletionContentPartParam) -> ChatCompletionMessageParam:
        if content['type'] != 'text':
            raise TypeError

        return {
            "role": "assistant",
            "content": [content],
        }

    @override
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> ChatCompletionMessageParam:
        if not isinstance(tool_input, str):
            raise TypeError

        return {
            "role": "assistant",
            "content": None,
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
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> ChatCompletionMessageParam:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_output,
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
    def tool_definition(self, name: str, desc: str, schema: dict) -> ChatCompletionToolParam:
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
    def tool_definitions(self, tools: list[ChatCompletionToolParam]) -> list[ChatCompletionToolParam] | None:
        return tools

    @override
    def tool_selection_none(self) -> ChatCompletionToolChoiceOptionParam | None:
        return 'none'

    @override
    def tool_selection_auto(self) -> ChatCompletionToolChoiceOptionParam | None:
        return 'auto'

    @override
    def tool_selection_any(self) -> ChatCompletionToolChoiceOptionParam | None:
        return 'required'

    @override
    def tool_selection_name(self, tool_name: str) -> ChatCompletionToolChoiceOptionParam | None:
        return {
            "type": 'function',
            "function": {
                "name": tool_name,
            },
        }
