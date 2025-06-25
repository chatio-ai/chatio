
import mimetypes

from collections.abc import Iterator

from dataclasses import dataclass

from os import PathLike
from pathlib import Path

from chatio.core.config import ModelConfig
from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.client import ApiClient

from chatio.core.events import CallEvent, DoneEvent, StatEvent, TextEvent


from .state import ChatState
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

        self._state = ChatState(state, tools)

        self._usage = ChatUsage()

    # streams

    def _process_tool_call(self, tool_call_id: str, tool_name: str, tool_args: dict) -> Iterator[dict]:
        tool_func = self._state().funcs.get(tool_name)
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

        self._state.commit_call_response(tool_call_id, tool_name, content)

    def __call__(self, content: str | None = None) -> Iterator[dict]:
        if content:
            self._state.commit_input_message(content)

        return self._iterate()

    def _iterate(self) -> Iterator[dict]:
        calls = -1
        while calls:
            calls = 0

            events = self._client.iterate_model_events(model=self._model.model, params=self._state())

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
                            self._state.commit_output_message(text)
                    case CallEvent(call_id, name, args, args_raw):
                        self._state.commit_call_request(call_id, name, args_raw)
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
            self._state.commit_input_message(content)

        return self._client.count_message_tokens(model=self._model.model, params=self._state())

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._model.vendor,
            self._model.model,
            len(self._state().funcs),
            bool(self._state().system),
            len(self._state().messages),
        )

    # history

    def attach_image_document(self, *, file: str | PathLike) -> None:
        with Path(file).open("rb") as filep:
            blob = filep.read()

            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

            self._state.commit_input_message(str(file))

            self._state.attach_image_document(blob, mimetype)

    def commit_input_message(self, message: str) -> None:
        self._state.commit_input_message(message)

    def commit_output_message(self, message: str) -> None:
        self._state.commit_output_message(message)

    def update_system_message(self, message: str | None) -> None:
        self._state.update_system_message(message)

    def use_prediction_content(self, message: str | None) -> None:
        self._state.use_prediction_content(message)
