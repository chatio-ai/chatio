
import base64

from typing import override

from anthropic.types import MessageParam

from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import DocumentBlockParam

from anthropic.types import ToolUseBlockParam
from anthropic.types import ToolResultBlockParam

from chatio.core.format.state_messages import ApiMessagesFormatterBase

from chatio.api.claude.config import ClaudeConfigFormat

from .state_options import text_message


type _ContentBlockParamBase = TextBlockParam | ImageBlockParam | DocumentBlockParam
type _InputContentBlockParam = _ContentBlockParamBase | ToolResultBlockParam
type _OutputContentBlockParam = _ContentBlockParamBase | ToolUseBlockParam


# pylint: disable=too-few-public-methods
class ClaudeMessagesFormatter(ApiMessagesFormatterBase[
    MessageParam,
    TextBlockParam,
    ImageBlockParam,
    DocumentBlockParam,
    ClaudeConfigFormat,
]):

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
                    case 'text' | 'image' | 'document' | 'tool_use' | 'tool_result':
                        entry.pop('cache_control', None)
                        last_entry = entry
                    case _:
                        raise TypeError

        if self._config.use_cache and last_entry is not None:
            last_entry.update({
                'cache_control': {
                    "type": "ephemeral",
                },
            })

        return messages

    @override
    def _chat_messages(self, messages: list[MessageParam]) -> list[MessageParam]:
        return self._setup_messages_cache(messages)

    @override
    def _text_message(self, text: str) -> TextBlockParam:
        return text_message(text)

    @override
    def _image_document_blob(self, blob: bytes, mimetype: str) -> ImageBlockParam:
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
    def _text_document_chunk(self, text: str, mimetype: str) -> DocumentBlockParam:
        match mimetype:
            case 'text/plain':
                pass
            case _:
                raise ValueError

        return {
            "type": "document",
            "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": text,
            },
        }

    @override
    def _input_content(self, content: _InputContentBlockParam) -> MessageParam:
        return {
            "role": "user",
            "content": [content],
        }

    @override
    def _output_content(self, content: _OutputContentBlockParam) -> MessageParam:
        return {
            "role": "assistant",
            "content": [content],
        }

    @override
    def _call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> MessageParam:
        return self._output_content({
            "type": "tool_use",
            "id": tool_call_id,
            "name": tool_name,
            "input": tool_input,
        })

    @override
    def _call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> MessageParam:
        return self._input_content({
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": tool_output,
        })
