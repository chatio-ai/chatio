
import base64
import logging
import mimetypes

from openai import OpenAI

from ._common import ChatBase


log = logging.getLogger(__name__)


class OpenAIStat:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.cached_tokens = 0


class OpenAIChat(ChatBase):
    def _setup_context(self, config):
        self._client = OpenAI(
                base_url=config.api_url,
                api_key=config.api_key)

        self._model = config.model

        self._stats = OpenAIStat()

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

    def _tool_schema(self, schema):
        result = schema.copy()

        if result.get("type") == "object":
            props = result.setdefault("properties", {})
        else:
            props = None

        if props is not None:
            result.update({
                "additionalProperties": False,
                "required": list(props),
            })

            for key in props:
                value = props.get(key, {})
                value = self._tool_schema(value)
                props[key] = value

        return result

    def _setup_tools(self, tools, tool_choice, tool_choice_name):
        self._tools = []
        self._funcs = {}

        if tools is None:
            tools = {}

        for name, tool in tools.items():
            desc = tool.__desc__
            schema = self._tool_schema(tool.__schema__)

            if not name or not desc or not schema:
                raise RuntimeError()

            self._tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": desc,
                    "parameters": schema,
                    "strict": True,
                },
            })

            self._funcs[name] = tool

        if not tool_choice:
            self._tool_choice = None
        elif not tool_choice_name:
            self._tool_choice = {"type": tool_choice}
        else:
            self._tool_choice = {"type": tool_choice, "function": {"name": tool_choice_name}}

    def _process_stats(self, usage):
        yield {
            "type": "token_stats",
            "scope": "round",
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "cache_written": 0,
            "cache_read": usage.prompt_tokens_details.cached_tokens,
        }

        self._stats.prompt_tokens += usage.prompt_tokens
        self._stats.completion_tokens += usage.completion_tokens
        self._stats.cached_tokens += usage.prompt_tokens_details.cached_tokens

        yield {
            "type": "token_stats",
            "scope": "total",
            "input_tokens": self._stats.prompt_tokens,
            "output_tokens": self._stats.completion_tokens,
            "cache_written": 0,
            "cache_read": self._stats.cached_tokens,
        }

    # messages

    def _as_contents(self, content):
        if isinstance(content, str):
            return [{"type": "text", "text": content}]
        elif isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content

        raise RuntimeError()

    def _format_user_message(self, content):
        return {
            "role": "user",
            "content": self._as_contents(content)
        }

    def _format_model_message(self, content):
        return {
            "role": "assistant",
            "content": self._as_contents(content)
        }

    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        return {
            "role": "assistant",
            "tool_calls": [{
                "id": tool_call_id,
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": tool_input,
                },
            }],
        }

    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_output,
        }

    def __call__(self, request):
        self._commit_user_message(request)

        tool_use_blocks = [request]
        while tool_use_blocks:
            tool_use_blocks = []

            if self._tools:
                stream = self._client.beta.chat.completions.stream(
                    model=self._model,
                    max_tokens=4096,
                    stream_options={'include_usage': True},
                    messages=self._messages,
                    tools=self._tools)
            else:
                stream = self._client.beta.chat.completions.stream(
                    model=self._model,
                    max_tokens=4096,
                    stream_options={'include_usage': True},
                    messages=self._messages)

            with stream as stream:

                for chunk in stream:
                    log.info("%s", chunk.to_dict())
                    if chunk.type == 'content.delta':
                        yield chunk.delta

                final = stream.get_final_completion().choices[0].message

                response = final.content
                if response:
                    if not response.endswith("\n"):
                        yield "\n"
                    self._commit_model_message(response)

                calls = final.tool_calls or ()
                for call in calls:
                    tool_use_blocks.append(call)
                    self._commit_tool_request(call.id,
                                              call.function.name,
                                              call.function.arguments)
                    yield {
                        "type": "tools_usage",
                        "tool_name": call.function.name,
                        "tool_args": call.function.parsed_arguments,
                    }

                usage = stream.get_final_completion().usage
                if usage:
                    yield from self._process_stats(usage)

            for tool_use_block in tool_use_blocks:
                content_chunks = []
                for chunk in self._run_tool(tool_use_block):
                    if isinstance(chunk, str):
                        content_chunks.append(chunk)
                        yield chunk
                    elif chunk is not None:
                        yield {
                            "type": "tools_event",
                            "tool_name": tool_use_block.function.name,
                            "tool_data": chunk,
                        }

                self._commit_tool_response(tool_use_block.id,
                                           tool_use_block.function.name,
                                           "".join(content_chunks))

    def _run_tool(self, content_block):
        func = self._funcs.get(content_block.function.name)
        if func is not None:
            yield from func(**content_block.function.parsed_arguments)

    @staticmethod
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
