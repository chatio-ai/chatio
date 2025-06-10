
from typing import override

from chatio.api._common import ChatFormat

from .params import ClaudeParams


class ClaudeFormat(ChatFormat):

    def __init__(self, params: ClaudeParams):
        self._params = params

    def _setup_cache(self, entry):
        if self._params.use_cache and entry:
            entry[-1].update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return entry

    def _setup_messages_cache(self, messages):
        for message in messages:
            for content in message.get("content"):
                content.pop("cache_control", None)

        if messages:
            self._setup_cache(messages[-1].get("content"))

        return messages

    # messages

    @override
    def chat_messages(self, messages):
        return self._setup_messages_cache(messages)

    @override
    def text_chunk(self, text):
        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_blob(self, blob, mimetype):
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": blob,
            },
        }

    @override
    def system_message(self, content):
        if not content:
            return [], []

        return self._setup_cache(self._as_contents(content)), []

    @override
    def input_message(self, content):
        return {
            "role": "user",
            "content": self._as_contents(content),
        }

    @override
    def output_message(self, content):
        return {
            "role": "assistant",
            "content": self._as_contents(content),
        }

    @override
    def tool_request(self, tool_call_id, tool_name, tool_input):
        return self.output_message({
            "type": "tool_use",
            "id": tool_call_id,
            "name": tool_name,
            "input": tool_input,
        })

    @override
    def tool_response(self, tool_call_id, tool_name, tool_output):
        return self.input_message({
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": tool_output,
        })

    # functions

    @override
    def tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    @override
    def tool_definitions(self, tools):
        return self._setup_cache(tools)

    @override
    def tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None

        if not tool_choice_name:
            return {
                "type": tool_choice,
            }

        return {
            "type": tool_choice,
            "name": tool_choice_name,
        }
