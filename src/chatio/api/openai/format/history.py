
import base64

from typing import override

import weasyprint

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionContentPartTextParam
from openai.types.chat import ChatCompletionContentPartImageParam
from openai.types.chat.chat_completion_content_part_param import File

from chatio.core.format.history import ApiFormatHistory

from chatio.api.openai.config import OpenAIConfig


type _ChatCompletionContentPartParam = \
    ChatCompletionContentPartTextParam | ChatCompletionContentPartImageParam | File


class OpenAIFormatHistory(ApiFormatHistory[
    ChatCompletionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    File,
    OpenAIConfig,
]):

    @override
    def chat_messages(self, messages: list[ChatCompletionMessageParam]) -> list[ChatCompletionMessageParam]:
        return messages

    @override
    def text_message(self, text: str) -> ChatCompletionContentPartTextParam:
        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_document_blob(self, blob: bytes, mimetype: str) -> ChatCompletionContentPartImageParam:
        data = base64.b64encode(blob).decode('ascii')

        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mimetype};base64,{data}",
            },
        }

    @override
    def text_document_chunk(self, text: str, mimetype: str) -> File:
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
