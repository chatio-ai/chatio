
from typing import override

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict
from google.genai.types import PartDict


from chatio.core.models import TextMessage
from chatio.core.models import CallRequest
from chatio.core.models import CallResponse
from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument

from chatio.core.format.state_messages import ApiMessagesFormatterBase

from chatio.api.google.config import GoogleConfigFormat


def message_text(msg: TextMessage) -> PartDict:
    return {
        "text": msg.text,
    }


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
    def _message_text(self, msg: TextMessage) -> PartDict:
        return message_text(msg)

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
    def _call_request(self, req: CallRequest) -> ContentDict:
        if not isinstance(req.tool_input, dict):
            raise TypeError

        return {
            "role": "model",
            "parts": [{
                "function_call": {
                    "id": req.tool_call_id,
                    "name": req.tool_name,
                    "args": req.tool_input,
                },
            }],
        }

    @override
    def _call_response(self, resp: CallResponse) -> ContentDict:
        return {
            "role": "user",
            "parts": [{
                "function_response": {
                    "id": resp.tool_call_id,
                    "name": resp.tool_name,
                    "response": {
                        "output": resp.tool_output,
                    },
                },
            }],
        }

    @override
    def _image_document_blob(self, doc: ImageDocument) -> PartDict:
        return {
            "inline_data": {
                "mime_type": doc.mimetype,
                "data": doc.blob,
            },
        }

    @override
    def _text_document_text(self, doc: TextDocument) -> PartDict:
        return {
            "inline_data": {
                "mime_type": doc.mimetype,
                "data": doc.text.encode(),
            },
        }
