
import base64
import logging
import mimetypes

from openai import OpenAI

from . import ChatBase


log = logging.getLogger(__name__)


class Stats:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0


class Chat(ChatBase):
    def _setup_context(self, model):
        self._client = OpenAI()
        if model is None:
            model = 'gpt-4o'

        self._model = model

        self._stats = Stats()

    def _setup_messages(self, system, messages):
        self._messages = []

        if system:
            self._messages.append({"role": "developer", "content": self._as_contents(system)})

        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            self._messages.append(
                    self._usr_message(message)
                    if not index % 2 else
                    self._bot_message(message))

    def _setup_tools(self, tools, tool_choice, tool_choice_name):
        # TODO

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

        if not tool_choice:
            self._tool_choice = None
        elif not tool_choice_name:
            self._tool_choice = {"type": tool_choice}
        else:
            self._tool_choice = {"type": tool_choice, "name": tool_choice_name}

    def _process_stats(self, usage):
        yield {
            "type": "token_stats",
            "scope": "round",
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "cache_written": 0,
            "cache_read": 0,
        }

        self._stats.prompt_tokens += usage.prompt_tokens
        self._stats.completion_tokens += usage.completion_tokens

        yield {
            "type": "token_stats",
            "scope": "total",
            "input_tokens": self._stats.prompt_tokens,
            "output_tokens": self._stats.completion_tokens,
            "cache_written": 0,
            "cache_read": 0,
        }

    def __call__(self, request):
        while request:
            self._messages.append(self._usr_message(request))

            tool_use_blocks = []

            with self._client.beta.chat.completions.stream(
                model=self._model,
                max_tokens=4096,
                stream_options={'include_usage': True},
                messages=self._messages) as stream:
                #tools=self._tools) as stream:

                for chunk in stream:
                    log.info("%s", chunk.to_dict())
                    if chunk.type == 'content.delta':
                        yield chunk.delta

                usage = stream.get_final_completion().usage
                if usage:
                    yield from self._process_stats(usage)

                response = stream.get_final_completion().choices[0].message.content
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
