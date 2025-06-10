
import base64
import mimetypes

from collections.abc import Iterator

from dataclasses import dataclass

from pathlib import Path

from pprint import pprint

from chatio.core.stats import ChatStats
from chatio.core.events import ChatEvent, CallEvent, DoneEvent, StatEvent, TextEvent


@dataclass
class ApiConfig:
    api_cls: str | None
    api_url: str | None = None
    api_key: str | None = None

    options: dict | None = None


@dataclass
class ApiParams:
    pass


@dataclass
class ChatConfig:
    vendor: str
    model: str

    config: ApiConfig


@dataclass
class ToolConfig:
    tools: dict | None = None
    tool_choice: str | None = None
    tool_choice_name: str | None = None


@dataclass
class ChatInfo:
    vendor: str
    model: str
    tools: int
    system: int
    messages: int


class ChatBase:

    def __init__(self,
                 system=None, messages=None,
                 tools: ToolConfig | None = None,
                 config: ChatConfig | None = None):

        self._ready = False

        if config is None:
            raise RuntimeError

        self._config = config

        self._setup_context(config.config)

        self._system = None

        self._messages: list[dict] = []

        self._setup_messages(system, messages)

        if tools is None:
            tools = ToolConfig()

        self._setup_tools(tools)

        self._stats = ChatStats()

    def _setup_context(self, config: ApiConfig):
        raise NotImplementedError

    # messages

    def _setup_messages(self, system, messages):
        self._system, self._messages = self._format_dev_message(system)

        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            if not index % 2:
                self._commit_user_message(message)
            else:
                self._commit_model_message(message)

    def _format_chat_messages(self, messages):
        return messages

    def _as_contents(self, content):
        if isinstance(content, str):
            chunk = self._format_text_chunk(content)
            return chunk if isinstance(chunk, str) else [chunk]
        if isinstance(content, dict):
            return [content]
        if isinstance(content, list):
            return content

        raise RuntimeError

    def _format_text_chunk(self, text):
        raise NotImplementedError

    def _format_dev_message(self, content):
        raise NotImplementedError

    def _format_user_message(self, content):
        raise NotImplementedError

    def _commit_user_message(self, content):
        self._messages.append(self._format_user_message(content))
        self._ready = True

    def _format_model_message(self, content):
        raise NotImplementedError

    def _commit_model_message(self, content):
        self._messages.append(self._format_model_message(content))
        self._ready = False

    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        raise NotImplementedError

    def _commit_tool_request(self, tool_call_id, tool_name, tool_input):
        self._messages.append(self._format_tool_request(tool_call_id, tool_name, tool_input))
        self._ready = False

    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        raise NotImplementedError

    def _commit_tool_response(self, tool_call_id, tool_name, tool_output):
        self._messages.append(self._format_tool_response(tool_call_id, tool_name, tool_output))
        self._ready = True

    # tools

    def _format_tool_definition(self, name, desc, schema):
        raise NotImplementedError

    def _format_tool_definitions(self, tools):
        return tools

    def _format_tool_selection(self, tool_choice, tool_choice_name):
        raise NotImplementedError

    def _setup_tools(self, tools: ToolConfig):
        self._tools = []
        self._funcs = {}

        if tools.tools is None:
            tools.tools = {}

        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            self._tools.append(self._format_tool_definition(name, desc, schema))

            self._funcs[name] = tool

        self._tools = self._format_tool_definitions(self._tools)

        # self._tool_choice = self._format_tool_selection(tools.tool_choice, tools.tool_choice_name)
        return self._format_tool_selection(tools.tool_choice, tools.tool_choice_name)

    def _process_tool(self, tool_call_id, tool_name, tool_args):
        tool_func = self._funcs.get(tool_name)
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

        self._commit_tool_response(tool_call_id, tool_name, content)

    # stream

    def _iterate_model_events(self, model, system, messages, tools) -> Iterator[ChatEvent]:
        raise NotImplementedError

    def __call__(self, content=None, **kwargs) -> Iterator[dict]:
        if content:
            self._commit_user_message(content)

        return self._iterate(**kwargs)

    def _iterate(self, **kwargs) -> Iterator[dict]:
        while self._ready:
            self._messages = self._format_chat_messages(self._messages)

            self._debug_base_chat_state()

            events = self._iterate_model_events(
                model=self._config.model,
                system=self._system,
                messages=self._messages,
                tools=self._tools,
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
                            self._commit_model_message(text)
                    case CallEvent(call_id, name, args, args_raw):
                        self._commit_tool_request(call_id, name, args_raw)
                        yield {
                            "type": "tools_usage",
                            "tool_name": name,
                            "tool_args": args,
                        }
                        yield from self._process_tool(call_id, name, args)
                    case StatEvent():
                        yield from self._stats(event)

    def _count_message_tokens(self, model, system, messages, tools):
        raise NotImplementedError

    def count_tokens(self, content=None):
        if content:
            self._commit_user_message(content)

        return self._count_message_tokens(
            model=self._config.model,
            system=self._system,
            messages=self._messages,
            tools=self._tools,
        )

    # debug

    def info(self):
        return ChatInfo(
            self._config.vendor,
            self._config.model,
            len(self._funcs or ()),
            len(self._system or ()),
            len(self._messages),
        )

    def _debug_base_chat_state(self):
        _debug = False
        # _debug = True

        if _debug:
            print()
            pprint(self._system)
            print()
            pprint(self._messages)
            print()

    # history

    def _format_image_blob(self, blob, mimetype):
        raise NotImplementedError

    def commit_image(self, filepath):
        with Path(filepath).open("rb") as file:
            data = file.read()
            blob = base64.b64encode(data).decode()
            mimetype, _ = mimetypes.guess_type(filepath)

            self._commit_user_message(filepath)

            self._commit_user_message(self._format_image_blob(blob, mimetype))

    def commit_chunk(self, chunk, *, model=False):
        if model:
            self._commit_model_message(chunk)
        else:
            self._commit_user_message(chunk)
