
import logging

from anthropic import Anthropic

from ._common import ChatBase

from ._events import *


log = logging.getLogger(__name__)


class ClaudePump:
    def __init__(self, stream):
        self._stream = stream

    def __iter__(self):
        with self._stream as stream:
            for chunk in stream:
                log.info("%s", chunk.to_dict())

                if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                    yield TextEvent(chunk.delta.text)

            yield DoneEvent(stream.get_final_text())

            for message in stream.get_final_message().content:
                if message.type == 'tool_use':
                    yield CallEvent(message.id, message.name, message.input, message.input)

            usage = stream.get_final_message().usage
            yield StatEvent(
                    usage.input_tokens, usage.output_tokens,
                    usage.cache_creation_input_tokens, usage.cache_read_input_tokens)


class ClaudeChat(ChatBase):
    def _setup_context(self, config, use_cache=True):
        self._client = Anthropic(
                base_url=config.api_url,
                api_key=config.api_key)

        self._cache = use_cache

    def _setup_cache(self, param):
        if self._cache and param:
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

    def _format_tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    def _format_tool_definitions(self, tools):
        return self._setup_cache(tools)

    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None
        elif not tool_choice_name:
            return {"type": tool_choice}
        else:
            return {"type": tool_choice, "name": tool_choice_name}

    # messages

    def _format_chat_messages(self, messages):
        return self._setup_messages_cache(messages)

    def _format_text_chunk(self, text):
        return {"type": "text", "text": text}

    def _format_image_blob(self, blob, mimetype):
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": blob,
            },
        }

    def _format_dev_message(self, content):
        if not content:
            return [], []

        return self._setup_cache(self._as_contents(content)), []

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
        return self._format_model_message({
            "type": "tool_use",
            "id": tool_call_id,
            "name": tool_name,
            "input": tool_input,
        })

    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        return self._format_user_message({
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": tool_output,
        })

    # events

    def _iterate_model_events(self, model, system, messages, tools):
        return ClaudePump(self._client.messages.stream(
            model=model,
            max_tokens=4096,
            tools=tools,
            system=system,
            messages=messages))

    # helpers

    def _count_message_tokens(self, model, system, messages, tools):
        return self._client.messages.count_tokens(
            model=model,
            tools=tools,
            system=system,
            messages=messages).input_tokens

