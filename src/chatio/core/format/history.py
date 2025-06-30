
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument
from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ContentEntry

from chatio.core.config import ApiConfigFormat

from ._common import ApiFormatBase


class ApiFormatHistory[
    MessageContentT,
    TextMessageT,
    ImageDocumentT,
    TextDocumentT,
    ApiConfigFormatT: ApiConfigFormat,
](
    ApiFormatBase[ApiConfigFormatT],
    ABC,
):

    @abstractmethod
    def chat_messages(self, messages: list[MessageContentT]) -> list[MessageContentT]:
        ...

    @abstractmethod
    def text_message(self, text: str) -> TextMessageT:
        ...

    @abstractmethod
    def text_document_chunk(self, text: str, mimetype: str) -> TextDocumentT:
        ...

    @abstractmethod
    def image_document_blob(self, blob: bytes, mimetype: str) -> ImageDocumentT:
        ...

    @abstractmethod
    def input_content(self, content: TextMessageT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def input_message(self, message: str) -> MessageContentT:
        return self.input_content(self.text_message(message))

    @abstractmethod
    def output_content(self, content: TextMessageT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def output_message(self, message: str) -> MessageContentT:
        return self.output_content(self.text_message(message))

    @abstractmethod
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> MessageContentT:
        ...

    @abstractmethod
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> MessageContentT:
        ...

    def image_document(self, blob: bytes, mimetype: str) -> MessageContentT:
        return self.input_content(self.image_document_blob(blob, mimetype))

    def text_document(self, text: str, mimetype: str) -> MessageContentT:
        return self.input_content(self.text_document_chunk(text, mimetype))

    def format(self, messages: list[ContentEntry]) -> list[MessageContentT]:
        _messages = []

        for message in messages:
            match message:
                case InputMessage(text):
                    _messages.append(self.input_message(text))
                case OutputMessage(text):
                    _messages.append(self.output_message(text))
                case CallRequest(tool_call_id, tool_name, tool_input):
                    _messages.append(self.call_request(tool_call_id, tool_name, tool_input))
                case CallResponse(tool_call_id, tool_name, tool_output):
                    _messages.append(self.call_response(tool_call_id, tool_name, tool_output))
                case TextDocument(text, mimetype):
                    _messages.append(self.text_document(text, mimetype))
                case ImageDocument(blob, mimetype):
                    _messages.append(self.image_document(blob, mimetype))
                case _:
                    raise RuntimeError(message)

        return self.chat_messages(_messages)


# pylint: disable=too-few-public-methods
class ApiFormatHistoryProto[MessageContentT](Protocol):

    @abstractmethod
    def format(self, messages: list[ContentEntry]) -> list[MessageContentT]:
        ...
