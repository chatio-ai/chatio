
import mimetypes

from dataclasses import dataclass

from os import PathLike
from pathlib import Path

from chatio.core.models import PredictionMessage
from chatio.core.models import SystemMessage

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument

from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ChatState as _ChatState


@dataclass
class ChatState(_ChatState):

    def __init__(self, prompt: str | None = None, messages: list[str] | None = None) -> None:
        super().__init__()

        if messages is not None:
            self.append_chat_messages(messages)

        self.update_system_message(prompt)

    def attach_image_document(self, *, file: str | PathLike, mimetype: str | None = None) -> None:
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

        self.messages.append(InputMessage(str(file)))

        blob = Path(file).read_bytes()
        self.messages.append(ImageDocument(blob, mimetype))

    def attach_text_document(self, *, file: str | PathLike, mimetype: str | None = None) -> None:
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

        self.messages.append(InputMessage(str(file)))

        text = Path(file).read_text(encoding="utf-8")
        self.messages.append(TextDocument(text, mimetype))

    def attach_document_auto(self, *, file: str | PathLike) -> None:
        mimetype, _ = mimetypes.guess_type(file)
        if mimetype is None:
            raise RuntimeError

        match mimetype:
            case "text/plain":
                return self.attach_text_document(file=file, mimetype=mimetype)
            case _:
                return self.attach_image_document(file=file, mimetype=mimetype)

    def append_input_message(self, message: str) -> None:
        self.messages.append(InputMessage(message))

    def append_output_message(self, message: str) -> None:
        self.messages.append(OutputMessage(message))

    def append_chat_messages(self, messages: list[str]) -> None:
        for index, message in enumerate(messages):
            if not index % 2:
                self.append_input_message(message)
            else:
                self.append_output_message(message)

    def append_call_response(self, call_id: str, name: str, args: str) -> None:
        self.messages.append(CallResponse(call_id, name, args))

    def append_call_request(self, call_id: str, name: str, args: str | dict[str, object]) -> None:
        self.messages.append(CallRequest(call_id, name, args))

    def update_system_message(self, message: str | None) -> None:
        self.options.system = None if message is None else SystemMessage(message)

    def update_prediction_message(self, message: str | None) -> None:
        self.options.prediction = None if message is None else PredictionMessage(message)
