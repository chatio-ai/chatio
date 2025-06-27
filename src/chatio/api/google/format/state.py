
from typing import override

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict
from google.genai.types import PartDict

from chatio.core.models import ContentEntry

from chatio.core.format.state import ApiFormatState
from chatio.core.params import ApiExtras

from chatio.api.google.config import GoogleConfig


class GoogleFormatState(ApiFormatState[
    ContentDict,
    ContentUnionDict,
    PartDict,
    PartDict,
    PartDict,
    ApiExtras,
]):

    def __init__(self, config: GoogleConfig):
        self._config = config

    @override
    def chat_messages(self, messages: list[ContentUnionDict]) -> list[ContentUnionDict]:
        return messages

    @override
    def text_message(self, text: str) -> PartDict:
        return {
            "text": text,
        }

    @override
    def text_document_chunk(self, text: str, mimetype: str) -> PartDict:
        return {
            "inline_data": {
                "mime_type": mimetype,
                "data": text.encode(),
            },
        }

    @override
    def image_document_blob(self, blob: bytes, mimetype: str) -> PartDict:
        return {
            "inline_data": {
                "mime_type": mimetype,
                "data": blob,
            },
        }

    @override
    def system_content(self, content: PartDict) -> ContentDict:
        return {
            "parts": [content],
        }

    @override
    def extras(self, extras: dict[str, ContentEntry | None]) -> ApiExtras:
        return ApiExtras()

    @override
    def input_content(self, content: PartDict) -> ContentDict:
        return {
            "role": "user",
            "parts": [content],
        }

    @override
    def output_content(self, content: PartDict) -> ContentDict:
        return {
            "role": "model",
            "parts": [content],
        }

    @override
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> ContentDict:
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
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> ContentDict:
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
