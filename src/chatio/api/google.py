
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
                "parameters": schema,
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

    # messages

    def _as_contents(self, content):
        if isinstance(content, str):
            return [{"text": content}]
        elif isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content

        raise RuntimeError()

    def _commit_dev_message(self, content):
        if not content:
            self._system = None
        else:
            self._system = {"parts": self._as_contents(content)}

    def _format_user_message(self, content):
        return {
            "role": "user",
            "parts": self._as_contents(content)
        }

    def _format_model_message(self, content):
        return {
            "role": "model",
            "parts": self._as_contents(content)
        }
    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        return {
            "role": "model",
            "parts": [{
                "function_call": {
                    "id": tool_call_id,
                    "name": tool_name,
                    "args": tool_input,
                },
            }],
        }

    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        return {
            "role": "user",
            "parts": [{
                "function_response": {
                    "id": tool_call_id,
                    "name": tool_name,
                    "response": {
                        "output": tool_output,
                    },
                },
            }],
        }

    def __call__(self, request):
        self._commit_user_message(request)

        tool_use_blocks = [request]
        while tool_use_blocks:
            tool_use_blocks = []

            stream = self._client.models.generate_content_stream(
                model=self._model,
                contents=self._messages,
                config={
                    'system_instruction': self._system,
                    'max_output_tokens': 4096,
                    'tools': [{
                        "function_declarations": self._tools,
                    }] if self._tools else None,
                })

            if stream:

                usage = None

                final_text = ""
                for chunk in stream:
                    log.info("%s", chunk.to_json_dict())
                    if chunk.candidates \
                            and chunk.candidates[0].content \
                            and chunk.candidates[0].content.parts:

                        for part in chunk.candidates[0].content.parts:
                            if part.text:
                                final_text += part.text
                                yield part.text
                            if part.function_call:
                                tool_use_blocks.append(part.function_call)
                                self._commit_tool_request(part.function_call.id,
                                                          part.function_call.name,
                                                          part.function_call.args)
                                yield {
                                    "type": "tools_usage",
                                    "tool_name": part.function_call.name,
                                    "tool_args": part.function_call.args,
                                }

                    usage = chunk.usage_metadata

                if usage:
                    yield from self._process_stats(usage)

                if final_text:
                    self._commit_model_message(final_text)

            for tool_use_block in tool_use_blocks:
                content_chunks = []
                for chunk in self._run_tool(tool_use_block.name, tool_use_block.args):
                    if isinstance(chunk, str):
                        content_chunks.append(chunk)
                        yield chunk
                    elif chunk is not None:
                        yield {
                            "type": "tools_event",
                            "tool_name": tool_use_block.name,
                            "tool_data": chunk,
                        }

                self._commit_tool_response(tool_use_block.id,
                                           tool_use_block.name,
                                           "".join(content_chunks))

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
