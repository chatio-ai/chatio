
import base64
import logging
import mimetypes

from anthropic import Anthropic


log = logging.getLogger(__name__)


class Chat:
    def __init__(self, system=None, messages=None, tools=None, tool_choice=None, tool_choice_name=None):
        self._client = Anthropic()

        if system is None:
            system = ""
        self._system = system

        if messages is None:
            messages = []

        self._messages = []
        for index, message in enumerate(messages):
            self._messages.append(
                    self._user_message(message)
                    if not index % 2 else
                    self._ai_message(message))

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

    def _user_message(self, content):
        return {"role": "user", "content": content}

    def _ai_message(self, content):
        return {"role": "assistant", "content": content}

    def __call__(self, request):
        while request:
            self._messages.append(self._user_message(request))

            tool_use_blocks = []

            with self._client.messages.stream(
                model='claude-3-5-sonnet-latest',
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
                        yield {
                            "type": "token_stats",
                            "input_tokens": chunk.message.usage.input_tokens,
                            "output_tokens": chunk.message.usage.output_tokens,
                        }

                response = [_.to_dict() for _ in stream.get_final_message().content]

                if response:
                    self._messages.append(self._ai_message(response))

            request = []
            for tool_use_block in tool_use_blocks:
                content_chunks = []
                for chunk in self._run_tool(tool_use_block):
                    if isinstance(chunk, str):
                        content_chunks.append(chunk)
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
