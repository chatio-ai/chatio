
import logging

from collections.abc import Iterator

from dataclasses import dataclass

from typing import override

from httpx import Client as HttpxClient

from anthropic import Anthropic
from anthropic.lib.streaming import MessageStreamManager


from chatio.core.events import ChatEvent, CallEvent, DoneEvent, StatEvent, TextEvent

from chatio.api._utils import httpx_args

from chatio.api._common import ApiConfig
from chatio.api._common import ApiParams
from chatio.api._common import ChatBase


log = logging.getLogger(__name__)


@dataclass
class ClaudeParams(ApiParams):
    use_cache: bool = True


def _pump(streamctx: MessageStreamManager) -> Iterator[ChatEvent]:
    with streamctx as stream:
        for chunk in stream:
            log.info("%s", chunk.model_dump_json(indent=2))

            if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                yield TextEvent(chunk.delta.text)

        yield DoneEvent(stream.get_final_text())

        final = stream.get_final_message()

        usage = final.usage
        usage.input_tokens += usage.cache_creation_input_tokens or 0
        usage.input_tokens += usage.cache_read_input_tokens or 0
        yield StatEvent(
            usage.input_tokens,
            usage.output_tokens,
            usage.cache_creation_input_tokens or 0,
            usage.cache_read_input_tokens or 0,
            0, 0)

        for message in final.content:
            if message.type == 'tool_use':
                yield CallEvent(message.id, message.name, message.input, message.input)


class ClaudeChat(ChatBase):

    @override
    def _setup_context(self, config: ApiConfig):
        self._client = Anthropic(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = ClaudeParams(**config.options if config.options else {})

    def _setup_cache(self, param):
        if self._params.use_cache and param:
            param[-1].update({"cache_control": {"type": "ephemeral"}})

        return param

    def _setup_messages_cache(self, messages):
        for message in messages:
            for content in message.get("content"):
                content.pop("cache_control", None)

        if messages:
            self._setup_cache(messages[-1].get("content"))

        return messages

    # tools

    @override
    def _format_tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    @override
    def _format_tool_definitions(self, tools):
        return self._setup_cache(tools)

    @override
    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None

        if not tool_choice_name:
            return {"type": tool_choice}

        return {"type": tool_choice, "name": tool_choice_name}

    # messages

    @override
    def _format_chat_messages(self, messages):
        return self._setup_messages_cache(messages)

    @override
    def _format_text_chunk(self, text):
        return {"type": "text", "text": text}

    @override
    def _format_image_blob(self, blob, mimetype):
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": blob,
            },
        }

    @override
    def _format_system_message(self, content):
        if not content:
            return [], []

        return self._setup_cache(self._as_contents(content)), []

    @override
    def _format_input_message(self, content):
        return {
            "role": "user",
            "content": self._as_contents(content),
        }

    @override
    def _format_output_message(self, content):
        return {
            "role": "assistant",
            "content": self._as_contents(content),
        }

    @override
    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        return self._format_output_message({
            "type": "tool_use",
            "id": tool_call_id,
            "name": tool_name,
            "input": tool_input,
        })

    @override
    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        return self._format_input_message({
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": tool_output,
        })

    # events

    @override
    def _iterate_model_events(self, model, system, messages, tools, **_kwargs) -> Iterator[ChatEvent]:
        return _pump(self._client.messages.stream(
            model=model,
            max_tokens=4096,
            tools=tools,
            system=system,
            messages=messages))

    # helpers

    @override
    def _count_message_tokens(self, model, system, messages, tools):
        return self._client.messages.count_tokens(
            model=model,
            tools=tools,
            system=system,
            messages=messages).input_tokens
