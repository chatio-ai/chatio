
import base64

from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import ToolUseBlockParam
from anthropic.types import ToolResultBlockParam


from chatio.core.format import ChatFormat

from .params import ClaudeParams


type _ContentBlockParamBase = TextBlockParam | ImageBlockParam
type _InputContentBlockParam = _ContentBlockParamBase | ToolResultBlockParam
type _OutputContentBlockParam = _ContentBlockParamBase | ToolUseBlockParam


class ClaudeFormat(ChatFormat[TextBlockParam, MessageParam, TextBlockParam, ImageBlockParam, ToolParam, ToolParam]):

    def __init__(self, params: ClaudeParams) -> None:
        self._params = params

    def _setup_tools_cache(self, entries: list[ToolParam]) -> list[ToolParam]:
        if self._params.use_cache and entries:
            entry = entries[-1]

            entry.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return entries

    def _setup_messages_cache(self, messages: list[MessageParam]) -> list[MessageParam]:
        last_entry = None

        for message in messages:
            content = message.get("content")

            if not isinstance(content, list):
                raise TypeError

            for entry in content:
                if not isinstance(entry, dict):
                    raise TypeError

                match entry['type']:
                    case 'text' | 'image' | 'tool_use' | 'tool_result':
                        entry.pop('cache_control', None)
                        last_entry = entry
                    case _:
                        raise TypeError

        if self._params.use_cache and last_entry is not None:
            last_entry.update({
                'cache_control': {
                    "type": "ephemeral",
                },
            })

        return messages

    # messages

    @override
    def chat_messages(self, messages: list[MessageParam]) -> list[MessageParam]:
        return self._setup_messages_cache(messages)

    @override
    def text_chunk(self, text: str) -> TextBlockParam:
        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_blob(self, blob: bytes, mimetype: str) -> ImageBlockParam:
        match mimetype:
            case 'image/jpeg' | 'image/png' | 'image/gif' | 'image/webp':
                pass
            case _:
                raise ValueError

        data = base64.b64encode(blob).decode('ascii')

        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": data,
            },
        }

    @override
    def system_content(self, content: TextBlockParam) -> TextBlockParam:
        if self._params.use_cache:
            content.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return content

    def _input_content(self, content: _InputContentBlockParam) -> MessageParam:
        return {
            "role": "user",
            "content": [content],
        }

    @override
    def input_content(self, content: _ContentBlockParamBase) -> MessageParam:
        return self._input_content(content)

    def _output_content(self, content: _OutputContentBlockParam) -> MessageParam:
        return {
            "role": "assistant",
            "content": [content],
        }

    @override
    def output_content(self, content: _ContentBlockParamBase) -> MessageParam:
        return self._output_content(content)

    @override
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> MessageParam:
        return self._output_content({
            "type": "tool_use",
            "id": tool_call_id,
            "name": tool_name,
            "input": tool_input,
        })

    @override
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> MessageParam:
        return self._input_content({
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": tool_output,
        })

    # functions

    @override
    def tool_definition(self, name: str, desc: str, schema: dict) -> ToolParam:
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    @override
    def tool_definitions(self, tools: list[ToolParam]) -> list[ToolParam]:
        return self._setup_tools_cache(tools)

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
            "name": tool_choice_name,
        }
