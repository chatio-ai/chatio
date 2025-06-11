
import base64
import mimetypes

from collections.abc import Iterator
from collections.abc import Callable

from dataclasses import dataclass

from os import PathLike
from pathlib import Path

from chatio.core.config import ToolConfig
from chatio.core.config import ChatApi

from chatio.core.events import CallEvent, DoneEvent, StatEvent, TextEvent


from .stats import ChatStats


@dataclass
class ChatInfo:
    vendor: str
    model: str
    tools: int
    system: int
    messages: int


@dataclass
class ChatState:
    system: list[dict] | dict | None
    messages: list[dict]
    tools: list[dict] | None
    funcs: dict[str, Callable]
    tool_choice: dict | None

    def __init__(self):
        self.system = None
        self.messages = []
        self.tools = None
        self.funcs = {}


class ChatBase:
    def __init__(self, api: ChatApi,
                 system: str | None = None,
                 messages: list[str] | None = None,
                 tools: ToolConfig | None = None) -> None:

        self._api = api

        self._ready = False

        self._state = ChatState()

        self._update_system_message(system)

        self._setup_message_history(messages)

        if tools is None:
            tools = ToolConfig()

        self._setup_tool_definitions(tools)

        self._stats = ChatStats()

    # messages

    def _commit_input_content(self, content: dict) -> None:
        self._state.messages.append(self._api.format.input_content(content))
        self._ready = True

    def _commit_input_message(self, message: str) -> None:
        self._commit_input_content(self._api.format.text_chunk(message))

    def _commit_output_content(self, content: dict) -> None:
        self._state.messages.append(self._api.format.output_content(content))
        self._ready = False

    def _commit_output_message(self, message: str) -> None:
        self._commit_output_content(self._api.format.text_chunk(message))

    def _commit_call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> None:
        self._state.messages.append(self._api.format.call_request(tool_call_id, tool_name, tool_input))
        self._ready = False

    def _commit_call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> None:
        self._state.messages.append(self._api.format.call_response(tool_call_id, tool_name, tool_output))
        self._ready = True

    def _update_system_message(self, message: str | None) -> None:
        if not message:
            self._state.system = None
            return

        self._state.system = self._api.format.system_content(self._api.format.text_chunk(message))

    def _setup_message_history(self, messages: list[str] | None) -> None:
        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            if not index % 2:
                self._commit_input_message(message)
            else:
                self._commit_output_message(message)

    def _setup_tool_definitions(self, tools: ToolConfig) -> None:
        self._state.tools = []
        self._state.funcs = {}

        if tools.tools is None:
            tools.tools = {}

        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            self._state.tools.append(self._api.format.tool_definition(name, desc, schema))

            self._state.funcs[name] = tool

        self._state.tools = self._api.format.tool_definitions(self._state.tools)

        self._state.tool_choice = self._api.format.tool_selection(tools.tool_choice, tools.tool_choice_name)

    # streams

    def _process_tool_call(self, tool_call_id: str, tool_name: str, tool_args: dict) -> Iterator[dict]:
        tool_func = self._state.funcs.get(tool_name)
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

        self._commit_call_response(tool_call_id, tool_name, content)

    def __call__(self, content: str | None = None, **kwargs) -> Iterator[dict]:
        if content:
            self._commit_input_message(content)

        return self._iterate(**kwargs)

    def _iterate(self, **kwargs) -> Iterator[dict]:
        while self._ready:
            self._state.messages = self._api.format.chat_messages(self._state.messages)

            events = self._api.client.iterate_model_events(
                model=self._api.config.model,
                system=self._state.system,
                messages=self._state.messages,
                tools=self._state.tools,
                **kwargs,
            )

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
                            self._commit_output_message(text)
                    case CallEvent(call_id, name, args, args_raw):
                        self._commit_call_request(call_id, name, args_raw)
                        yield {
                            "type": "tools_usage",
                            "tool_name": name,
                            "tool_args": args,
                        }
                        yield from self._process_tool_call(call_id, name, args)
                    case StatEvent():
                        yield from self._stats(event)

    # helpers

    def count_tokens(self, content: str | None = None) -> int:
        if content:
            self._commit_input_message(content)

        return self._api.client.count_message_tokens(
            model=self._api.config.model,
            system=self._state.system,
            messages=self._state.messages,
            tools=self._state.tools,
        )

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._api.config.vendor,
            self._api.config.model,
            len(self._state.funcs),
            bool(self._state.system),
            len(self._state.messages),
        )

    # history

    def attach_image_content(self, *, file: str | PathLike) -> None:
        with Path(file).open("rb") as filep:
            data = filep.read()
            blob = base64.b64encode(data).decode()

            mimetype, _ = mimetypes.guess_type(file)
            if mimetype is None:
                raise RuntimeError

            self._commit_input_message(str(file))

            self._commit_input_content(self._api.format.image_blob(blob, mimetype))

    def commit_input_message(self, message: str) -> None:
        self._commit_input_message(message)

    def commit_output_message(self, message: str) -> None:
        self._commit_output_message(message)

    def update_system_message(self, message: str | None) -> None:
        self._update_system_message(message)
