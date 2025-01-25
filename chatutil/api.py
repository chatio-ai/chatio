
import base64
import mimetypes

from anthropic import Anthropic

class Chat:
    def __init__(self, system=None, messages=None, tools=None):
        self._client = Anthropic()

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

        for tool in tools:
            name = tool.get("name")
            func = tool.pop("func")

            if not name or not func:
                raise RuntimeError()

            self._funcs.setdefault(name, func)
            self._tools.append(tool)

    def _user_message(self, content):
        return {"role": "user", "content": content}

    def _ai_message(self, content):
        return {"role": "assistant", "content": content}

    def __call__(self, request):

        self._messages.append(self._user_message(request))

        tool_use_block = None

        with self._client.messages.stream(
            model='claude-3-5-sonnet-latest',
            max_tokens=4096,
            system=self._system,
            messages=self._messages,
            tools=self._tools) as stream:

            for chunk in stream:
                if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                    yield chunk.delta.text
                elif chunk.type == 'content_block_stop' and chunk.content_block.type == 'tool_use':
                    tool_use_block = chunk.content_block

            response = [_.to_dict() for _ in stream.get_final_message().content]

            self._messages.append(self._ai_message(response))

        if tool_use_block:
            yield from self._run_tool(tool_use_block)

    def _run_tool(self, content_block):
        func = self._funcs.get(content_block.name)
        if func is not None:
            content = func(**content_block.input)

        return self([{
            "type": "tool_result",
            "tool_use_id": content_block.id,
            "content": content,
        }])


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
