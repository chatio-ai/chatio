
import base64
import logging
import mimetypes

from openai import OpenAI

from ._common import ChatBase


log = logging.getLogger(__name__)


class OpenAIChat(ChatBase):
    def _setup_context(self, config):
        self._client = OpenAI(
                base_url=config.api_url,
                api_key=config.api_key)

        self._model = config.model

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

    def _chat__iter__(self, tools, messages):

        stream = self._client.beta.chat.completions.stream(
            model=self._model,
            max_tokens=4096,
            stream_options={'include_usage': True},
            messages=messages,
            tools=tools)

        with stream as stream:

            for chunk in stream:
                log.info("%s", chunk.to_dict())
                if chunk.type == 'content.delta':
                    yield {
                        "type": "text",
                        "text": chunk.delta,
                    }

            final = stream.get_final_completion().choices[0].message
            yield {
                "type": "done",
                "text": final.content,
            }

            for call in final.tool_calls or ():
                yield {
                    "type": "call",
                    "call": {
                        "id": call.id,
                        "name": call.function.name,
                        "args": call.function.parsed_arguments,
                        "input": call.function.arguments,
                    }
                }

            usage = stream.get_final_completion().usage
            yield {
                "type": "stat",
                "stat": {
                    "input_tokens": usage.prompt_tokens,
                    "output_tokens": usage.completion_tokens,
                    "cache_written": 0,
                    "cache_read": usage.prompt_tokens_details.cached_tokens,
                },
            }

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
