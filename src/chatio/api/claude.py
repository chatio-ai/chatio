
import base64
import logging
import mimetypes

from anthropic import Anthropic

from ._common import ChatBase

from ._events import *


log = logging.getLogger(__name__)


class ClaudePump:
    def __init__(self, model, system, messages, tools, client=None):
        self._model = model
        self._tools = tools
        self._system = system
        self._messages = messages

        self._client = client

    def __iter__(self):
        stream = self._client.messages.stream(
            model=self._model,
            max_tokens=4096,
            system=self._system,
            messages=self._messages,
            tools=self._tools)

        with stream as stream:
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

    # tools

    def _format_tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "input_schema": schema,
        }

    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None
        elif not tool_choice_name:
            return {"type": tool_choice}
        else:
            return {"type": tool_choice, "name": tool_choice_name}

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
        self._setup_cache(tools)
        self._setup_messages_cache(messages)

        return ClaudePump(model, system, messages, tools, self._client)

    # helpers

    def _token_count(self):
        return self._client.messages.count_tokens(
                model=self._model,
                system=self._system,
                messages=self._messages,
                tools=self._tools).input_tokens

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
