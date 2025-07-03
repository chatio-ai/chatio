
import base64

from typing import override

import weasyprint

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat.chat_completion_content_part_param import File

from chatio.core.format.state_messages import ApiMessagesFormatterBase

from chatio.api.openai.config import OpenAIConfigFormat

from .state_options import message_text


type _ChatCompletionContentPartParam = \
    ChatCompletionContentPartTextParam | ChatCompletionContentPartImageParam | File


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
    def _message_text(self, text: str) -> ChatCompletionContentPartTextParam:
        return message_text(text)

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
    def _call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> ChatCompletionMessageParam:
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
    def _call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> ChatCompletionMessageParam:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_output,
        }

    @override
    def _image_document_blob(self, blob: bytes, mimetype: str) -> ChatCompletionContentPartImageParam:
        data = base64.b64encode(blob).decode('ascii')

        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mimetype};base64,{data}",
            },
        }

    @override
    def _text_document_text(self, text: str, mimetype: str) -> File:
        blob = weasyprint.HTML(string=f"<html><body><pre>{text}</pre></body></html>").write_pdf()
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
