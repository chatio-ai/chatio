
import base64
import logging
import mimetypes

from google.genai import Client

from ._common import ChatBase
from ._common import ChatConfig


log = logging.getLogger(__name__)


class GoogleStat:
    def __init__(self):
        self.cached_content_token_count = 0
        self.candidates_token_count = 0
        self.prompt_token_count = 0


class GoogleChat(ChatBase):
    def _setup_context(self, config: ChatConfig):
        self._client = Client(
                #base_url=config.api_url,
                api_key=config.api_key)

        self._model = config.model

        self._stats = GoogleStat()

    def _setup_messages(self, system, messages):
        if not system:
            self._system = None
        else:
            self._system = {"parts": self._as_contents(system)}

        if messages is None:
            messages = []

        self._messages = []
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
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "cache_written": 0,
            "cache_read": usage.cached_content_token_count or 0,
        }

        self._stats.prompt_token_count += usage.prompt_token_count
        self._stats.candidates_token_count += usage.candidates_token_count
        self._stats.cached_content_token_count += usage.cached_content_token_count or 0

        yield {
            "type": "token_stats",
            "scope": "total",
            "input_tokens": self._stats.prompt_token_count,
            "output_tokens": self._stats.candidates_token_count,
            "cache_written": 0,
            "cache_read": self._stats.cached_content_token_count,
        }

    def _as_contents(self, content):
        if isinstance(content, str):
            return [{"text": content}]
        else:
            return content

    def _usr_message(self, content):
        return {"role": "user", "parts": self._as_contents(content)}

    def _bot_message(self, content, tool_calls=None):
        message = {"role": "model", "parts": self._as_contents(content)}
        if tool_calls:
            message.update({"tool_calls": tool_calls})
        return message

    def __call__(self, request):
        self._messages.append(self._usr_message(request))

        done = False
        while not done:

            tool_use_blocks = []

            stream = self._client.models.generate_content_stream(
                model=self._model,
                contents=self._messages,
                config={
                    'system_instruction': self._system,
                    'max_output_tokens': 4096,
                })

            if stream:

                usage = None
                final_content = ""
                for chunk in stream:
                    log.info("%s", chunk.to_json_dict())
                    if chunk.candidates \
                            and chunk.candidates[0].content \
                            and chunk.candidates[0].content.parts:
                        chunk_content = "".join(part.text for part in chunk.candidates[0].content.parts)
                        final_content += chunk_content
                        yield chunk_content

                    usage = chunk.usage_metadata

                #calls = final.choices[0].message.tool_calls
                #if calls:
                #    for call in calls:
                #        tool_use_blocks.append(call)
                #        yield {
                #            "type": "tools_usage",
                #            "tool_name": call.function.name,
                #            "tool_args": call.function.parsed_arguments,
                #        }

                if usage:
                    yield from self._process_stats(usage)

                if final_content:
                    self._messages.append(self._bot_message(final_content))

            yield "\n"

            if not tool_use_blocks:
                done = True

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

                self._messages.append({
                    "role": "tool",
                    "tool_call_id": tool_use_block.id,
                    "content": "".join(content_chunks),
                })

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
