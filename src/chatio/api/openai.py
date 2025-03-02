
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

    # tools

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

    def _format_tool_definition(self, name, desc, schema):
        schema = self._tool_schema(schema)
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": schema,
                "strict": True,
            },
        }

    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None
        elif not tool_choice_name:
            return {"type": tool_choice}
        else:
            return {"type": tool_choice, "function": {"name": tool_choice_name}}

    # stats

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

    def _format_dev_message(self, content):
        return {
            "role": "developer",
            "content": self._as_contents(content)
        }

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

        tool_calls = [request]
        while tool_calls:
            tool_calls = []

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
                    tool_calls.append((
                        call.id,
                        call.function.name,
                        call.function.parsed_arguments,
                    ))
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

            yield from self._process_tools(tool_calls)

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
