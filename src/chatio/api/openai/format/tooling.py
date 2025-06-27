
from typing import override

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from chatio.core.format.tooling import ApiFormatTooling

from chatio.api.openai.config import OpenAIConfig


class OpenAIFormatTooling(ApiFormatTooling[
    ChatCompletionToolParam,
    list[ChatCompletionToolParam],
    ChatCompletionToolChoiceOptionParam,
    OpenAIConfig,
]):

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
