
from typing import override

from chatio.core.format import ChatFormat

from .params import ClaudeParams


class ClaudeFormat(ChatFormat):

    def __init__(self, params: ClaudeParams):
        self._params = params

    def _setup_cache(self, entries: list[dict]) -> list[dict]:
        if self._params.use_cache and entries:
            entries[-1].update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return entries

    def _setup_messages_cache(self, messages: list[dict]) -> list[dict]:
        content: list[dict] | None = None

        for message in messages:
            content = message.get("content")
            if content is not None:
                for entry in content:
                    entry.pop("cache_control", None)

        if messages:
            content = messages[-1].get("content")
            if content is not None:
                self._setup_cache(content)

        return messages

    # messages

    @override
    def chat_messages(self, messages: list[dict]) -> list[dict]:
        return self._setup_messages_cache(messages)

    @override
    def text_chunk(self, text: str) -> dict:
        return {
            "type": "text",
            "text": text,
        }

    @override
    def image_blob(self, blob: str, mimetype: str) -> dict:
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": blob,
            },
        }

    @override
    def system_message(self, content: str | None) -> tuple[list[dict], list[dict]]:
        if not content:
            return [], []

        return self._setup_cache(self._as_contents(content)), []

    @override
    def input_content(self, content: dict) -> dict:
        return {
            "role": "user",
            "content": self._as_contents(content),
        }

    @override
    def output_content(self, content: dict) -> dict:
        return {
            "role": "assistant",
            "content": self._as_contents(content),
        }

    @override
    def tool_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> dict:
        return self.output_content({
            "type": "tool_use",
            "id": tool_call_id,
            "name": tool_name,
            "input": tool_input,
        })

    @override
    def tool_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> dict:
        return self.input_content({
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": tool_output,
        })

    # functions

    @override
    def tool_definition(self, name: str, desc: str, schema: dict) -> dict:
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    @override
    def tool_definitions(self, tools: list[dict]) -> list[dict]:
        return self._setup_cache(tools)

    @override
    def tool_selection(self, tool_choice: str | None, tool_choice_name: str | None) -> dict | None:
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
