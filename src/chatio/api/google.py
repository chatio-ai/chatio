
import logging

from collections.abc import Iterator
from collections.abc import Callable

from dataclasses import dataclass

from typing import override

from google.genai.types import GenerateContentResponse
from google.genai.types import GroundingMetadata
from google.genai.types import HttpOptions
from google.genai import Client

from html2text import HTML2Text


from chatio.core.events import ChatEvent, CallEvent, DoneEvent, StatEvent, TextEvent

from ._utils import httpx_args

from ._common import ApiConfig
from ._common import ApiParams
from ._common import ChatBase


log = logging.getLogger(__name__)


@dataclass
class GoogleParams(ApiParams):
    grounding: bool = False


def _pump_grounding(search: GroundingMetadata | None) -> Iterator[ChatEvent]:
    if search is None:
        return

    if search.grounding_chunks is not None:
        for index, chunk in enumerate(search.grounding_chunks, 1):
            uri, title = "", ""
            if chunk.web is not None and chunk.web.uri is not None:
                uri = chunk.web.uri
            if chunk.web is not None and chunk.web.title is not None:
                title = chunk.web.title
            entry = f"   [{index}]: <{uri}> {title}\n"
            yield TextEvent(entry, label="search.sources")

    if search.search_entry_point is not None:
        parser = HTML2Text(bodywidth=0)
        parser.inline_links = False
        parser.protect_links = True
        entry = parser.handle(search.search_entry_point.rendered_content or "")
        yield TextEvent(entry, label="search.suggest")


def _pump(streamfun: Callable[[], Iterator[GenerateContentResponse]]) -> Iterator[ChatEvent]:
    stream = streamfun()

    if stream is not None:

        usage = None
        calls = []
        final_text = ""
        search = None

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
                search = chunk.candidates[0].grounding_metadata

        for event in _pump_grounding(search):
            if event is not None:
                yield event

        yield DoneEvent(final_text)

        yield StatEvent(
            (usage and usage.prompt_token_count) or 0,
            (usage and usage.candidates_token_count) or 0,
            0, (usage and usage.cached_content_token_count) or 0,
            0, 0)

        for call in calls:
            yield CallEvent(call.id or "", call.name or "", call.args, call.args)


class GoogleChat(ChatBase):

    @override
    def _setup_context(self, config: ApiConfig):
        self._client = Client(
            # base_url=config.api_url,
            api_key=config.api_key,
            http_options=HttpOptions(client_args=httpx_args()))

        self._params = GoogleParams(**config.options if config.options else {})

    # tools

    @override
    def _format_tool_definition(self, name, desc, schema):
        return {
            "name": name,
            "description": desc,
            "parameters": schema,
        }

    @override
    def _format_tool_definitions(self, tools):
        tools_config = []

        if tools:
            tools_config.append({
                "function_declarations": tools,
            })

        if self._params.grounding:
            tools_config.append({
                "google_search": {},
            })

        if not tools_config:
            return None

        return tools_config

    @override
    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None

        if not tool_choice_name:
            return {"type": tool_choice}

        return {"type": tool_choice, "function": {"name": tool_choice_name}}

    # messages

    @override
    def _format_text_chunk(self, text):
        return {"text": text}

    @override
    def _format_image_blob(self, blob, mimetype):
        return {"inline_data": {
            "mime_type": mimetype,
            "data": blob,
        }}

    @override
    def _format_dev_message(self, content):
        if not content:
            return None, []

        return {"parts": self._as_contents(content)}, []

    @override
    def _format_user_message(self, content):
        return {
            "role": "user",
            "parts": self._as_contents(content),
        }

    @override
    def _format_model_message(self, content):
        return {
            "role": "model",
            "parts": self._as_contents(content),
        }

    @override
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

    @override
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

    @override
    def _iterate_model_events(self, model, system, messages, tools, **_kwargs) -> Iterator[ChatEvent]:
        return _pump(lambda: self._client.models.generate_content_stream(
            model=model,
            config={
                'max_output_tokens': 4096,
                'tools': tools,
                'system_instruction': system,
            },
            contents=messages))

    @override
    def _count_message_tokens(self, model, system, messages, tools):
        raise NotImplementedError
