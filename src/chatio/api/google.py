
import base64
import logging
import mimetypes

from google.genai import Client

from ._common import ChatBase
from ._common import ChatConfig


log = logging.getLogger(__name__)


class GoogleChat(ChatBase):
    def _setup_context(self, config: ChatConfig):
        self._client = Client(
                #base_url=config.api_url,
                api_key=config.api_key)

        self._model = config.model

    # tools

    def _format_tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "parameters": schema,
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

    def _chat__iter__(self, tools, messages):
        stream = self._client.models.generate_content_stream(
            model=self._model,
            contents=messages,
            config={
                'system_instruction': self._system,
                'max_output_tokens': 4096,
                'tools': [{
                    "function_declarations": tools,
                }] if tools else None,
            })

        if stream:

            usage = None
            calls = []
            final_text = ""

            for chunk in stream:
                log.info("%s", chunk.to_json_dict())

                if chunk.candidates \
                        and chunk.candidates[0].content \
                        and chunk.candidates[0].content.parts:

                    for part in chunk.candidates[0].content.parts:
                        if part.text:
                            final_text += part.text
                            yield {
                                "type": "text",
                                "text": part.text,
                            }

                        if part.function_call:
                            calls.append(part.function_call)

                    usage = chunk.usage_metadata

            yield {
                "type": "done",
                "text": final_text,
            }

            for call in calls:
                yield {
                    "type": "call",
                    "call": {
                        "id": call.id,
                        "name": call.name,
                        "args": call.args,
                        "input": call.args,
                    }
                }

            yield {
                "type": "stat",
                "stat": {
                    "input_tokens": usage.prompt_token_count,
                    "output_tokens": usage.candidates_token_count,
                    "cache_written": 0,
                    "cache_read": usage.cached_content_token_count or 0,
                }
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
