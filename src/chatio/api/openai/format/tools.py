
from collections.abc import Mapping

from typing import Any
from typing import override

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai.types import FunctionParameters

from openai import Omit, omit

from chatio.core.models import ToolSchema

from chatio.core.format.tools import ApiToolSchemasFormat
from chatio.core.format.tools import ApiToolChoiceFormat


# pylint: disable=too-few-public-methods
class OpenAIToolSchemasFormat(ApiToolSchemasFormat[
    list[ChatCompletionToolParam] | Omit,
    ChatCompletionToolParam,
]):

    def _tool_params_schema(self, params: Mapping[str, Any]) -> FunctionParameters:
        params_ = {**params}

        props = None
        if params_.get("type") == "object":
            props = params_.setdefault("properties", {})

        if props is not None:
            params_.update({
                "additionalProperties": False,
                "required": list(props),
            })

            for key in props:
                value = props.get(key, {})
                value = self._tool_params_schema(value)
                props[key] = value

        return params_

    @override
    def _tool_schema(self, schema: ToolSchema) -> ChatCompletionToolParam:
        params_ = self._tool_params_schema(schema.params)
        return {
            "type": "function",
            "function": {
                "name": schema.name,
                "description": schema.desc,
                "parameters": params_,
                "strict": True,
            },
        }

    @override
    def _tools(self, *schemas: ChatCompletionToolParam) -> list[ChatCompletionToolParam] | Omit:
        if not schemas:
            return omit
        return list(schemas)


class OpenAIToolChoiceFormat(ApiToolChoiceFormat[
    ChatCompletionToolChoiceOptionParam | Omit,
]):

    @override
    def _tool_choice_null(self) -> Omit:
        return omit

    @override
    def _tool_choice_none(self) -> ChatCompletionToolChoiceOptionParam:
        return "none"

    @override
    def _tool_choice_auto(self) -> ChatCompletionToolChoiceOptionParam:
        return "auto"

    @override
    def _tool_choice_any(self) -> ChatCompletionToolChoiceOptionParam:
        return "required"

    @override
    def _tool_choice_name(self, name: str) -> ChatCompletionToolChoiceOptionParam:
        return {
            "type": "function",
            "function": {
                "name": name,
            },
        }
