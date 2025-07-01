
import base64

from typing import override

import weasyprint

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat.chat_completion_content_part_param import File


from chatio.core.models import TextMessage
from chatio.core.models import CallRequest
from chatio.core.models import CallResponse
from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument

from chatio.core.format.state_messages import ApiMessagesFormatterBase

from chatio.api.openai.config import OpenAIConfigFormat


type _ChatCompletionContentPartParam = \
    ChatCompletionContentPartTextParam | ChatCompletionContentPartImageParam | File


def message_text(msg: TextMessage) -> ChatCompletionContentPartTextParam:
    return {
        "type": "text",
        "text": msg.text,
    }


# pylint: disable=too-few-public-methods
class OpenAIMessagesFormatter(ApiMessagesFormatterBase[
    ChatCompletionMessageParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    File,
    OpenAIConfigFormat,
]):

    @override
    def _chat_messages(self, messages: list[ChatCompletionMessageParam]) -> list[ChatCompletionMessageParam]:
        return messages

    @override
    def _message_text(self, msg: TextMessage) -> ChatCompletionContentPartTextParam:
        return message_text(msg)

    @override
    def _input_content(self, content: _ChatCompletionContentPartParam) -> ChatCompletionMessageParam:
        if content['type'] != 'text':
            return {
                "role": "user",
                "content": [content],
            }

        return {
            "role": "user",
            "content": content['text'] if self._config.legacy else [content],
        }

    @override
    def _output_content(self, content: _ChatCompletionContentPartParam) -> ChatCompletionMessageParam:
        if content['type'] != 'text':
            raise TypeError

        return {
            "role": "assistant",
            "content": [content],
        }

    @override
    def _call_request(self, req: CallRequest) -> ChatCompletionMessageParam:
        if not isinstance(req.tool_input, str):
            raise TypeError

        return {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": req.tool_call_id,
                "type": "function",
                "function": {
                    "name": req.tool_name,
                    "arguments": req.tool_input,
                },
            }],
        }

    @override
    def _call_response(self, resp: CallResponse) -> ChatCompletionMessageParam:
        return {
            "role": "tool",
            "tool_call_id": resp.tool_call_id,
            "content": resp.tool_output,
        }

    @override
    def _image_document_blob(self, doc: ImageDocument) -> ChatCompletionContentPartImageParam:
        data = base64.b64encode(doc.blob).decode('ascii')

        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{doc.mimetype};base64,{data}",
            },
        }

    @override
    def _text_document_text(self, doc: TextDocument) -> File:
        blob = weasyprint.HTML(string=f"<html><body><pre>{doc.text}</pre></body></html>").write_pdf()
        if blob is None:
            raise RuntimeError
        data = base64.b64encode(blob).decode('ascii')

        mimetype = 'application/pdf'

        return {
            "type": "file",
            "file": {
                "filename": "",
                "file_data": f"data:{mimetype};base64,{data}",
            },
        }
