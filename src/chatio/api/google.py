
import logging

from google.genai import Client

from ._common import ChatBase
from ._common import ChatConfig

from ._events import *


log = logging.getLogger(__name__)


class GooglePump:
    def __init__(self, stream):
        self._stream = stream

    def __iter__(self):
        stream = self._stream
        if stream:

            usage = None
            calls = []
            final_text = ""

            for chunk in stream:
                log.info("%s", chunk.model_dump_json(indent=2))

                if chunk.candidates \
                        and chunk.candidates[0].content \
                        and chunk.candidates[0].content.parts:

                    for part in chunk.candidates[0].content.parts:
                        if part.text:
                            final_text += part.text
                            yield TextEvent(part.text)

                        if part.function_call:
                            calls.append(part.function_call)

                    usage = chunk.usage_metadata

            yield DoneEvent(final_text)

            yield StatEvent(
                    usage.prompt_token_count or 0,
                    usage.candidates_token_count or 0,
                    0, usage.cached_content_token_count or 0,
                    0, 0)

            for call in calls:
                yield CallEvent(call.id, call.name, call.args, call.args)


class GoogleChat(ChatBase):
    def _setup_context(self, config: ChatConfig):
        self._client = Client(
                #base_url=config.api_url,
                api_key=config.api_key)

    # tools

    def _format_tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "parameters": schema,
        }

    def _format_tool_definitions(self, tools):
        return [{
            "function_declarations": tools,
        }] if tools else None

    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None
        elif not tool_choice_name:
            return {"type": tool_choice}
        else:
            return {"type": tool_choice, "function": {"name": tool_choice_name}}

    # messages

    def _format_text_chunk(self, text):
        return {"text": text}

    def _format_image_blob(self, blob, mimetype):
        return {"inline_data": {
            "mime_type": mimetype,
            "data": blob,
        }}

    def _format_dev_message(self, content):
        if not content:
            return None, []

        return {"parts": self._as_contents(content)}, []

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

    # events

    def _iterate_model_events(self, model, system, messages, tools, **kwargs):
        return GooglePump(self._client.models.generate_content_stream(
            model=model,
            config={
                'max_output_tokens': 4096,
                'tools': tools,
                'system_instruction': system,
            },
            contents=messages))
