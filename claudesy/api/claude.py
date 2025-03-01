
import base64
import logging
import mimetypes

from anthropic import Anthropic

from . import ChatBase


log = logging.getLogger(__name__)


class Stats:
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache_creation_input_tokens = 0
        self.cache_read_input_tokens = 0


class Chat(ChatBase):
    def _setup_context(self, config, use_cache=True):
        self._client = Anthropic(
                base_url=config.api_url,
                api_key=config.api_key)

        self._model = config.model
        self._cache = use_cache

        self._stats = Stats()

    def _setup_cache(self, param):
        if self._cache and param:
            param[-1].update({"cache_control": {"type": "ephemeral"}})

    def _setup_messages_cache(self):
        for message in self._messages:
            for content in message.get("content"):
                content.pop("cache_control", None)

        if self._messages:
            self._setup_cache(self._messages[-1].get("content"))

    def _setup_messages(self, system, messages):
        if not system:
            self._system = ""
        else:
            self._system = self._as_contents(system)
            self._setup_cache(self._system)

        if messages is None:
            messages = []

        self._messages = []
        for index, message in enumerate(messages):
            self._messages.append(
                    self._usr_message(message)
                    if not index % 2 else
                    self._bot_message(message))

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

            self._tools.append({
                "name": name,
                "description": desc,
                "input_schema": schema,
            })

            self._funcs[name] = tool

        self._setup_cache(self._tools)

        if not tool_choice:
            self._tool_choice = None
        elif not tool_choice_name:
            self._tool_choice = {"type": tool_choice}
        else:
            self._tool_choice = {"type": tool_choice, "name": tool_choice_name}

    def _token_count(self):
        return self._client.messages.count_tokens(
                model=self._model,
                system=self._system,
                messages=self._messages,
                tools=self._tools).input_tokens

    def _process_stats(self, usage):
        yield {
            "type": "token_stats",
            "scope": "round",
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cache_written": usage.cache_creation_input_tokens,
            "cache_read": usage.cache_read_input_tokens,
        }

        self._stats.input_tokens += usage.input_tokens
        self._stats.output_tokens += usage.output_tokens
        self._stats.cache_creation_input_tokens += usage.cache_creation_input_tokens
        self._stats.cache_read_input_tokens += usage.cache_read_input_tokens

        yield {
            "type": "token_stats",
            "scope": "total",
            "input_tokens": self._stats.input_tokens,
            "output_tokens": self._stats.output_tokens,
            "cache_written": self._stats.cache_creation_input_tokens,
            "cache_read": self._stats.cache_read_input_tokens,
        }

    def __call__(self, request):
        while request:
            self._messages.append(self._usr_message(request))

            self._setup_messages_cache()

            tool_use_blocks = []

            with self._client.messages.stream(
                model=self._model,
                max_tokens=4096,
                system=self._system,
                messages=self._messages,
                tools=self._tools) as stream:

                for chunk in stream:
                    log.info("%s", chunk.to_dict())
                    if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                        yield chunk.delta.text
                    elif chunk.type == 'content_block_stop' and chunk.content_block.type == 'tool_use':
                        tool_use_blocks.append(chunk.content_block)
                        yield {
                            "type": "tools_usage",
                            "tool_name": chunk.content_block.name,
                            "tool_args": chunk.content_block.input,
                        }
                    elif chunk.type == 'message_stop':
                        yield from self._process_stats(chunk.message.usage)

                response = [_.to_dict() for _ in stream.get_final_message().content]

                if response:
                    self._messages.append(self._bot_message(response))

            yield "\n"

            request = []
            for tool_use_block in tool_use_blocks:
                content_chunks = []
                for chunk in self._run_tool(tool_use_block):
                    if isinstance(chunk, str):
                        content_chunks.append(chunk)
                        yield chunk
                    elif chunk is not None:
                        yield {
                            "type": "tools_event",
                            "tool_name": tool_use_block.name,
                            "tool_data": chunk,
                        }

                request.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": "".join(content_chunks),
                })

    def _run_tool(self, content_block):
        func = self._funcs.get(content_block.name)
        if func is not None:
            yield from func(**content_block.input)

def do_image(filename):
    content = []

    with open(filename, "rb") as file:
        data = file.read()
        data_as_base64 = base64.b64encode(data)
        data_as_string = data_as_base64.decode()
        mimetype, _ = mimetypes.guess_type(filename)

        content.append({
            "type": "text",
            "text": filename,
        })

        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": data_as_string,
            }
        })

    return content
