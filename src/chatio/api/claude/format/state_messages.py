
import base64

from typing import override

from anthropic.types import MessageParam

from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam
from anthropic.types import DocumentBlockParam

from anthropic.types import ToolUseBlockParam
from anthropic.types import ToolResultBlockParam


from chatio.core.models import ChatMessage
from chatio.core.models import TextMessage
from chatio.core.models import CallRequest
from chatio.core.models import CallResponse
from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument

from chatio.core.format.state_messages import ApiMessagesFormatterBase

from chatio.api.claude.config import ClaudeConfigFormat


type _ContentBlockParamBase = TextBlockParam | ImageBlockParam | DocumentBlockParam
type _InputContentBlockParam = _ContentBlockParamBase | ToolResultBlockParam
type _OutputContentBlockParam = _ContentBlockParamBase | ToolUseBlockParam


def message_text(msg: TextMessage) -> TextBlockParam:
    return {
        "type": "text",
        "text": msg.text,
    }


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
    def _message_text(self, msg: TextMessage) -> TextBlockParam:
        return message_text(msg)

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
    def _call_request(self, req: CallRequest) -> MessageParam:
        return self._output_content({
            "type": "tool_use",
            "id": req.tool_call_id,
            "name": req.tool_name,
            "input": req.tool_input,
        })

    @override
    def _call_response(self, resp: CallResponse) -> MessageParam:
        return self._input_content({
            "type": "tool_result",
            "tool_use_id": resp.tool_call_id,
            "content": resp.tool_output,
        })

    @override
    def _image_document_blob(self, doc: ImageDocument) -> ImageBlockParam:
        match doc.mimetype:
            case 'image/jpeg' | 'image/png' | 'image/gif' | 'image/webp':
                pass
            case _:
                raise ValueError

        data = base64.b64encode(doc.blob).decode('ascii')

        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": doc.mimetype,
                "data": data,
            },
        }

    @override
    def _text_document_text(self, doc: TextDocument) -> DocumentBlockParam:
        match doc.mimetype:
            case 'text/plain':
                pass
            case _:
                raise ValueError

        return {
            "type": "document",
            "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": doc.text,
            },
            "citations": {
                "enabled": True,
            },
        }

    @override
    def _should_format(self, message: ChatMessage) -> bool:
        return bool(message)
