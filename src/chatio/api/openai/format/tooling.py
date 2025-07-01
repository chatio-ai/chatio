
from typing import override

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import NotGiven, NOT_GIVEN


from chatio.core.format.tooling import ApiToolingFormatterBase

from chatio.api.openai.config import OpenAIConfigFormat


# pylint: disable=too-few-public-methods
class OpenAIToolingFormatter(ApiToolingFormatterBase[
    list[ChatCompletionToolParam] | NotGiven,
    ChatCompletionToolParam,
    ChatCompletionToolChoiceOptionParam | NotGiven,
    OpenAIConfigFormat,
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
    def _tool_schema(self, name: str, desc: str, params: dict) -> ChatCompletionToolParam:
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
    def _tool_definitions(
        self, tools: list[ChatCompletionToolParam] | None,
    ) -> list[ChatCompletionToolParam] | NotGiven:

        if tools is None:
            return NOT_GIVEN
        return tools

    @override
    def _tool_choice_null(self) -> NotGiven:
        return NOT_GIVEN

    @override
    def _tool_choice_none(self) -> ChatCompletionToolChoiceOptionParam:
        return 'none'

    @override
    def _tool_choice_auto(self) -> ChatCompletionToolChoiceOptionParam:
        return 'auto'

    @override
    def _tool_choice_any(self) -> ChatCompletionToolChoiceOptionParam:
        return 'required'

    @override
    def _tool_choice_name(self, tool_name: str) -> ChatCompletionToolChoiceOptionParam:
        return {
            "type": 'function',
            "function": {
                "name": tool_name,
            },
        }
