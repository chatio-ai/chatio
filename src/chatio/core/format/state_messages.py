
from abc import ABC, abstractmethod

from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage
from chatio.core.models import TextMessage

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument
from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ChatMessage


# pylint: disable=too-few-public-methods
class ApiMessagesFormat[
    ChatMessageT,
    MessageTextT,
    ImageDocumentT,
    TextDocumentT,
](ABC):

    @abstractmethod
    def _chat_messages(self, *messages: ChatMessageT) -> list[ChatMessageT]:
        ...

    @abstractmethod
    def _message_text(self, msg: TextMessage) -> MessageTextT:
        ...

    @abstractmethod
    def _input_content(
            self, content: MessageTextT | ImageDocumentT | TextDocumentT) -> ChatMessageT:
        ...

    def _input_message(self, msg: InputMessage) -> ChatMessageT:
        return self._input_content(self._message_text(msg))

    @abstractmethod
    def _output_content(
            self, content: MessageTextT | ImageDocumentT | TextDocumentT) -> ChatMessageT:
        ...

    def _output_message(self, msg: OutputMessage) -> ChatMessageT:
        return self._output_content(self._message_text(msg))

    @abstractmethod
    def _call_request(self, req: CallRequest) -> ChatMessageT:
        ...

    @abstractmethod
    def _call_response(self, resp: CallResponse) -> ChatMessageT:
        ...

    @abstractmethod
    def _image_document_blob(self, doc: ImageDocument) -> ImageDocumentT:
        ...

    def _image_document(self, doc: ImageDocument) -> ChatMessageT:
        return self._input_content(self._image_document_blob(doc))

    @abstractmethod
    def _text_document_text(self, doc: TextDocument) -> TextDocumentT:
        ...

    def _text_document(self, doc: TextDocument) -> ChatMessageT:
        return self._input_content(self._text_document_text(doc))

    def _message(self, message: ChatMessage) -> ChatMessageT:
        match message:
            case InputMessage():
                return self._input_message(message)
            case OutputMessage():
                return self._output_message(message)
            case CallRequest():
                return self._call_request(message)
            case CallResponse():
                return self._call_response(message)
            case ImageDocument():
                return self._image_document(message)
            case TextDocument():
                return self._text_document(message)
            case _:
                raise RuntimeError(message)

    def __call__(self, messages: list[ChatMessage]) -> list[ChatMessageT]:
        return self._chat_messages(*(self._message(message) for message in messages if message))
