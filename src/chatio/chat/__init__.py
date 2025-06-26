
import mimetypes

from collections.abc import Iterator

from dataclasses import dataclass

from os import PathLike
from pathlib import Path

from chatio.core.config import ModelConfig
from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.models import PredictMessage
from chatio.core.models import SystemMessage
from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ImageDocument
from chatio.core.models import TextDocument
from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.client import ApiClient

from chatio.core.events import CallEvent, DoneEvent, StatEvent, TextEvent


from .usage import ChatUsage


@dataclass
class ChatInfo:
    vendor: str
    model: str
    tools: int
    system: int
    messages: int


class ChatBase:

    def __init__(
        self,
        client: ApiClient,
        model: ModelConfig,
        state: StateConfig | None = None,
        tools: ToolsConfig | None = None,
    ) -> None:

        self._client = client

        self._model = model

        self._state = ChatState.build(state)

        self._tools = ChatTools.build(tools)

        self._usage = ChatUsage()

    # streams

    def _process_tool_call(self, tool_call_id: str, tool_name: str, tool_args: dict) -> Iterator[dict]:
        tool_func = self._tools.funcs.get(tool_name)
        if not tool_func:
            return

        content = ""
        for chunk in tool_func(**tool_args):
            if isinstance(chunk, str):
                content += chunk
                yield {
                    "type": "tools_chunk",
                    "text": chunk,
                }
            elif chunk is not None:
                yield {
                    "type": "tools_event",
                    "tool_name": tool_name,
                    "tool_data": chunk,
                }

        self._state.messages.append(CallResponse(tool_call_id, tool_name, content))

    def __call__(self, content: str | None = None) -> Iterator[dict]:
        if content:
            self._state.messages.append(InputMessage(content))

        return self._iterate()

    def _iterate(self) -> Iterator[dict]:
        calls = -1
        while calls:
            calls = 0

            events = self._client.iterate_model_events(self._model.model, self._state, self._tools)

            for event in events:
                match event:
                    case TextEvent(text, label):
                        yield {
                            "type": "model_chunk",
                            "label": label,
                            "text": text,
                        }
                    case DoneEvent(text):
                        if text:
                            self._state.messages.append(OutputMessage(text))
                    case CallEvent(call_id, name, args, args_raw):
                        self._state.messages.append(CallRequest(call_id, name, args_raw))
                        yield {
                            "type": "tools_usage",
                            "tool_name": name,
                            "tool_args": args,
                        }
                        yield from self._process_tool_call(call_id, name, args)
                        calls += 1
                    case StatEvent():
                        yield from self._usage(event)

    # helpers

    def count_tokens(self, content: str | None = None) -> int:
        if content:
            self._state.messages.append(InputMessage(content))

        return self._client.count_message_tokens(self._model.model, self._state, self._tools)

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._model.vendor,
            self._model.model,
            len(self._tools.funcs),
            bool(self._state.system),
            len(self._state.messages),
        )

    # history

    def attach_image_document(self, *, file: str | PathLike, mimetype: str | None = None) -> None:
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

        self._state.messages.append(InputMessage(str(file)))

        with Path(file).open("rb") as filep:
            self._state.messages.append(ImageDocument(filep.read(), mimetype))

    def attach_text_document(self, *, file: str | PathLike, mimetype: str | None = None) -> None:
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

        self._state.messages.append(InputMessage(str(file)))

        with Path(file).open("r") as filep:
            self._state.messages.append(TextDocument(filep.read(), mimetype))

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
        self._state.messages.append(InputMessage(message))

    def commit_output_message(self, message: str) -> None:
        self._state.messages.append(InputMessage(message))

    def update_system_message(self, message: str | None) -> None:
        self._state.system = SystemMessage(message) if message is not None else None

    def use_prediction_content(self, message: str | None) -> None:
        _predict = PredictMessage(message) if message is not None else None
        self._state.extras.update({'prediction': _predict})
