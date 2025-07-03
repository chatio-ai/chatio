
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument
from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import MessageContent

from chatio.core.config import ApiConfigFormat

from ._base import ApiFormatBase


# pylint: disable=too-few-public-methods
class ApiMessagesFormatterBase[
    MessageContentT,
    MessageTextT,
    ImageDocumentT,
    TextDocumentT,
    ApiConfigFormatT: ApiConfigFormat,
](
    ApiFormatBase[ApiConfigFormatT],
    ABC,
):

    @abstractmethod
    def _chat_messages(self, messages: list[MessageContentT]) -> list[MessageContentT]:
        ...

    @abstractmethod
    def _message_text(self, text: str) -> MessageTextT:
        ...

    @abstractmethod
    def _input_content(self, content: MessageTextT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def _input_message(self, message: str) -> MessageContentT:
        return self._input_content(self._message_text(message))

    @abstractmethod
    def _output_content(self, content: MessageTextT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def _output_message(self, message: str) -> MessageContentT:
        return self._output_content(self._message_text(message))

    @abstractmethod
    def _call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> MessageContentT:
        ...

    @abstractmethod
    def _call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> MessageContentT:
        ...

    @abstractmethod
    def _image_document_blob(self, blob: bytes, mimetype: str) -> ImageDocumentT:
        ...

    def _image_document(self, blob: bytes, mimetype: str) -> MessageContentT:
        return self._input_content(self._image_document_blob(blob, mimetype))

    @abstractmethod
    def _text_document_text(self, text: str, mimetype: str) -> TextDocumentT:
        ...

    def _text_document(self, text: str, mimetype: str) -> MessageContentT:
        return self._input_content(self._text_document_text(text, mimetype))

    def format(self, messages: list[MessageContent]) -> list[MessageContentT]:
        _messages = []

        for message in messages:
            match message:
                case InputMessage(text):
                    _messages.append(self._input_message(text))
                case OutputMessage(text):
                    _messages.append(self._output_message(text))
                case CallRequest(tool_call_id, tool_name, tool_input):
                    _messages.append(self._call_request(tool_call_id, tool_name, tool_input))
                case CallResponse(tool_call_id, tool_name, tool_output):
                    _messages.append(self._call_response(tool_call_id, tool_name, tool_output))
                case TextDocument(text, mimetype):
                    _messages.append(self._text_document(text, mimetype))
                case ImageDocument(blob, mimetype):
                    _messages.append(self._image_document(blob, mimetype))
                case _:
                    raise RuntimeError(message)

        return self._chat_messages(_messages)


# pylint: disable=too-few-public-methods
class ApiMessagesFormatter[MessageContentT](Protocol):

    @abstractmethod
    def format(self, messages: list[MessageContent]) -> list[MessageContentT]:
        ...
