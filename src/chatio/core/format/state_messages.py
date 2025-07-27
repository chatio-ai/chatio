
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage
from chatio.core.models import TextMessage

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
    def _message_text(self, msg: TextMessage) -> MessageTextT:
        ...

    @abstractmethod
    def _input_content(
            self, content: MessageTextT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def _input_message(self, msg: InputMessage) -> MessageContentT:
        return self._input_content(self._message_text(msg))

    @abstractmethod
    def _output_content(
            self, content: MessageTextT | ImageDocumentT | TextDocumentT) -> MessageContentT:
        ...

    def _output_message(self, msg: OutputMessage) -> MessageContentT:
        return self._output_content(self._message_text(msg))

    @abstractmethod
    def _call_request(self, req: CallRequest) -> MessageContentT:
        ...

    @abstractmethod
    def _call_response(self, resp: CallResponse) -> MessageContentT:
        ...

    @abstractmethod
    def _image_document_blob(self, doc: ImageDocument) -> ImageDocumentT:
        ...

    def _image_document(self, doc: ImageDocument) -> MessageContentT:
        return self._input_content(self._image_document_blob(doc))

    @abstractmethod
    def _text_document_text(self, doc: TextDocument) -> TextDocumentT:
        ...

    def _text_document(self, doc: TextDocument) -> MessageContentT:
        return self._input_content(self._text_document_text(doc))

    def format(self, messages: list[MessageContent]) -> list[MessageContentT]:
        _messages = []

        for message in messages:
            match message:
                case InputMessage():
                    _messages.append(self._input_message(message))
                case OutputMessage():
                    _messages.append(self._output_message(message))
                case CallRequest():
                    _messages.append(self._call_request(message))
                case CallResponse():
                    _messages.append(self._call_response(message))
                case ImageDocument():
                    _messages.append(self._image_document(message))
                case TextDocument():
                    _messages.append(self._text_document(message))
                case _:
                    raise RuntimeError(message)

        return self._chat_messages(_messages)


# pylint: disable=too-few-public-methods
class ApiMessagesFormatter[MessageContentT](Protocol):

    @abstractmethod
    def format(self, messages: list[MessageContent]) -> list[MessageContentT]:
        ...
