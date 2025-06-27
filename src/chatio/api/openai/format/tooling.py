
from typing import override

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from chatio.core.format.tooling import ApiFormatTooling

from chatio.api.openai.config import OpenAIConfig


class OpenAIFormatTooling(ApiFormatTooling[
    list[ChatCompletionToolParam],
    ChatCompletionToolParam,
    ChatCompletionToolChoiceOptionParam,
    OpenAIConfig,
]):

    def _tool_params_schema(self, params: dict) -> dict:
        _params = params.copy()

        props = None
        if _params.get("type") == "object":
            props = _params.setdefault("properties", {})

        if props is not None:
            _params.update({
                "additionalProperties": False,
                "required": list(props),
            })

            for key in props:
                value = props.get(key, {})
                value = self._tool_params_schema(value)
                props[key] = value

        return _params

    @override
    def tool_schema(self, name: str, desc: str, params: dict) -> ChatCompletionToolParam:
        _params = self._tool_params_schema(params)
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": _params,
                "strict": True,
            },
        }

    @override
    def tool_definitions(self, tools: list[ChatCompletionToolParam]) -> list[ChatCompletionToolParam] | None:
        return tools

    @override
    def tool_choice_none(self) -> ChatCompletionToolChoiceOptionParam | None:
        return 'none'

    @override
    def tool_choice_auto(self) -> ChatCompletionToolChoiceOptionParam | None:
        return 'auto'

    @override
    def tool_choice_any(self) -> ChatCompletionToolChoiceOptionParam | None:
        return 'required'

    @override
    def tool_choice_name(self, tool_name: str) -> ChatCompletionToolChoiceOptionParam | None:
        return {
            "type": 'function',
            "function": {
                "name": tool_name,
            },
        }
