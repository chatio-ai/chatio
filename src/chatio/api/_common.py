
import json

import base64
import mimetypes

from dataclasses import dataclass

from ._events import *


class ChatConfig:

    def __init__(self, configpath=None):
        self._config = self._fromfile(configpath)

        self.model = self._config.get('model')
        self.api_key = self._config.get('api_key')
        self.api_url = self._config.get('api_url')
        self.api_type = self._config.get('api_type')

    def _validate(self):
        pass

    def _fromfile(self, configpath):
        if configpath is None:
            return {}

        try:
            with open(configpath, 'r') as configfp:
                return json.load(configfp)
        except FileNotFoundError:
            return {}


@dataclass
class ChatInfo:
    model: str
    tools: int
    system: int
    messages: int


@dataclass
class ChatStat:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_written: int = 0
    cache_read: int = 0


class ChatBase:

    def __init__(self,
                 system=None, messages=None,
                 tools=None, tool_choice=None, tool_choice_name=None,
                 config: ChatConfig = None, **kwargs):

        self._model = config.model

        self._setup_context(config, **kwargs)

        self._setup_messages(system, messages)

        self._setup_tools(tools, tool_choice, tool_choice_name)

        self._stats = ChatStat()

    def _setup_context(self, config: ChatConfig, **kwargs):
        raise NotImplementedError()

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
            return [self._format_text_chunk(content)]
        elif isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content

        raise RuntimeError()

    def _format_text_chunk(self, text):
        raise NotImplementedError()

    def _format_dev_message(self, content):
        raise NotImplementedError()

    def _commit_dev_message(self, content):
        self._messages.append(self._format_dev_message(content))

    def _format_user_message(self, content):
        raise NotImplementedError()

    def _commit_user_message(self, content):
        self._messages.append(self._format_user_message(content))

    def _format_model_message(self, content):
        raise NotImplementedError()

    def _commit_model_message(self, content):
        self._messages.append(self._format_model_message(content))

    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        raise NotImplementedError()

    def _commit_tool_request(self, tool_call_id, tool_name, tool_input):
        self._messages.append(self._format_tool_request(tool_call_id, tool_name, tool_input))

    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        raise NotImplementedError()

    def _commit_tool_response(self, tool_call_id, tool_name, tool_output):
        self._messages.append(self._format_tool_response(tool_call_id, tool_name, tool_output))

    # tools

    def _format_tool_definition(self, name, desc, schema):
        raise NotImplementedError()

    def _format_tool_definitions(self, tools):
        return tools

    def _format_tool_selection(self, tool_choice, tool_choice_name):
        raise NotImplementedError()

    def _setup_tools(self, tools, tool_choice, tool_choice_name):
        self._tools = []
        self._funcs = {}

        if tools is None:
            tools = {}

        for name, tool in tools.items():
            desc = tool.__desc__
            schema = tool.__schema__

            if not name or not desc or not schema:
                raise RuntimeError()

            self._tools.append(self._format_tool_definition(name, desc, schema))

            self._funcs[name] = tool

        self._tools = self._format_tool_definitions(self._tools)

        self._tool_choice = self._format_tool_selection(tool_choice, tool_choice_name)

    def _process_tool(self, tool_name, tool_args):
        func = self._funcs.get(tool_name)
        if func is not None:
            yield from func(**tool_args)

    def _process_tools(self, tool_calls):
        for tool_call in tool_calls:
            content_chunks = []
            for chunk in self._process_tool(tool_call.name, tool_call.args):
                if isinstance(chunk, str):
                    content_chunks.append(chunk)
                    yield chunk
                elif chunk is not None:
                    yield {
                        "type": "tools_event",
                        "tool_name": tool_call.name,
                        "tool_data": chunk,
                    }

            self._commit_tool_response(tool_call.call_id, tool_call.name, "".join(content_chunks))

    # stats

    def _process_stats(self, usage):
        yield {
            "type": "token_stats",
            "scope": "round",
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cache_written": usage.cache_written,
            "cache_read": usage.cache_read,
        }

        self._stats.input_tokens += usage.input_tokens
        self._stats.output_tokens += usage.output_tokens
        self._stats.cache_written += usage.cache_written
        self._stats.cache_read += usage.cache_read

        yield {
            "type": "token_stats",
            "scope": "total",
            "input_tokens": self._stats.input_tokens,
            "output_tokens": self._stats.output_tokens,
            "cache_written": self._stats.cache_written,
            "cache_read": self._stats.cache_read,
        }

    # debug

    def info(self):
        return ChatInfo(
            self._model,
            len(self._funcs or ()),
            len(self._system or ()),
            len(self._messages),
        )

    def _debug_base_chat_state(self):
        self._debug = False
        #self._debug = True

        if self._debug:
            from pprint import pprint
            print()
            pprint(self.system)
            print()
            pprint(self.messages)
            print()

    # stream

    def _iterate_model_events(self, model, system, messages, tools):
        raise NotImplementedError()

    def __call__(self, content=None):
        if content:
            self._commit_user_message(content)

        tool_calls = [content]
        while tool_calls:
            tool_calls = []

            self._messages = self._format_chat_messages(self._messages)

            self._debug_base_chat_state()

            events = self._iterate_model_events(
                model=self._model,
                system=self._system,
                messages=self._messages,
                tools=self._tools,
            )

            for event in events:
                match event:
                    case TextEvent(text):
                        yield text
                    case DoneEvent(text):
                        text = text or ""
                        if not text.endswith("\n"):
                            yield "\n"

                        if text:
                            self._commit_model_message(text)
                    case CallEvent(call_id, name, args, input):
                        tool_calls.append(event)
                        self._commit_tool_request(call_id, name, input)
                        yield {
                            "type": "tools_usage",
                            "tool_name": name,
                            "tool_args": args,
                        }
                    case StatEvent():
                        yield from self._process_stats(event)

            yield from self._process_tools(tool_calls)

    def commit_image(self, filepath):
        with open(filepath, "rb") as file:
            data = file.read()
            blob = base64.b64encode(data).decode()
            mimetype, _ = mimetypes.guess_type(filepath)

            self._commit_user_message(filepath)

            self._commit_user_message(self._format_image_blob(blob, mimetype))

    def _count_message_tokens(self, model, system, messages, tools):
        raise NotImplementedError()

    def count_tokens(self, content=None):
        if content:
            self._commit_user_message(content)

        return self._count_message_tokens(
            model=self._model,
            system=self._system,
            messages=self._messages,
            tools=self._tools,
        )
