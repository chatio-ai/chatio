
import mimetypes

from dataclasses import dataclass

from os import PathLike
from pathlib import Path

from chatio.core.config import StateConfig

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument

from chatio.core.models import PredictMessage
from chatio.core.models import SystemMessage
from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ChatState as _ChatState


@dataclass
class ChatState(_ChatState):

    def attach_image_document(self, *, file: str | PathLike, mimetype: str | None = None) -> None:
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

        self.messages.append(InputMessage(str(file)))

        with Path(file).open("rb") as filep:
            self.messages.append(ImageDocument(filep.read(), mimetype))

    def attach_text_document(self, *, file: str | PathLike, mimetype: str | None = None) -> None:
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

        self.messages.append(InputMessage(str(file)))

        with Path(file).open("r") as filep:
            self.messages.append(TextDocument(filep.read(), mimetype))

    def attach_document_auto(self, *, file: str | PathLike) -> None:
        mimetype, _ = mimetypes.guess_type(file)
        if mimetype is None:
            raise RuntimeError

        match mimetype:
            case "text/plain":
                return self.attach_text_document(file=file, mimetype=mimetype)
            case _:
                return self.attach_image_document(file=file, mimetype=mimetype)

    def commit_input_message(self, message: str) -> None:
        self.messages.append(InputMessage(message))

    def commit_call_response(self, call_id: str, name: str, args: str) -> None:
        self.messages.append(CallResponse(call_id, name, args))

    def commit_output_message(self, message: str) -> None:
        self.messages.append(InputMessage(message))

    def commit_call_request(self, call_id: str, name: str, args: object) -> None:
        self.messages.append(CallRequest(call_id, name, args))

    def update_system_message(self, message: str | None) -> None:
        self.system = SystemMessage(message) if message is not None else None

    def update_prediction_state(self, message: str | None) -> None:
        _predict = PredictMessage(message) if message is not None else None
        self.options.update({'prediction': _predict})


def build_state(state: StateConfig | None = None) -> ChatState:
    _state = ChatState()

    if state is None:
        state = StateConfig()

    if state.system is not None:
        _state.system = SystemMessage(state.system)

    if state.messages is None:
        state.messages = []

    for index, message in enumerate(state.messages):
        if not index % 2:
            _state.messages.append(InputMessage(message))
        else:
            _state.messages.append(OutputMessage(message))

    return _state
