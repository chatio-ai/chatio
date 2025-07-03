
from typing import override

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict
from google.genai.types import PartDict

from chatio.core.format.state_messages import ApiMessagesFormatterBase

from chatio.api.google.config import GoogleConfigFormat

from .state_options import message_text


# pylint: disable=too-few-public-methods
class GoogleMessagesFormatter(ApiMessagesFormatterBase[
    ContentUnionDict,
    PartDict,
    PartDict,
    PartDict,
    GoogleConfigFormat,
]):

    @override
    def _chat_messages(self, messages: list[ContentUnionDict]) -> list[ContentUnionDict]:
        return messages

    @override
    def _message_text(self, text: str) -> PartDict:
        return message_text(text)

    @override
    def _input_content(self, content: PartDict) -> ContentDict:
        return {
            "role": "user",
            "parts": [content],
        }

    @override
    def _output_content(self, content: PartDict) -> ContentDict:
        return {
            "role": "model",
            "parts": [content],
        }

    @override
    def _call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> ContentDict:
        if not isinstance(tool_input, dict):
            raise TypeError

        return {
            "role": "model",
            "parts": [{
                "function_call": {
                    "id": tool_call_id,
                    "name": tool_name,
                    "args": tool_input,
                },
            }],
        }

    @override
    def _call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> ContentDict:
        return {
            "role": "user",
            "parts": [{
                "function_response": {
                    "id": tool_call_id,
                    "name": tool_name,
                    "response": {
                        "output": tool_output,
                    },
                },
            }],
        }

    @override
    def _image_document_blob(self, blob: bytes, mimetype: str) -> PartDict:
        return {
            "inline_data": {
                "mime_type": mimetype,
                "data": blob,
            },
        }

    @override
    def _text_document_text(self, text: str, mimetype: str) -> PartDict:
        return {
            "inline_data": {
                "mime_type": mimetype,
                "data": text.encode(),
            },
        }
