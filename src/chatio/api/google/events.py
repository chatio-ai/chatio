
import logging

from collections.abc import Iterator
from collections.abc import Callable

from dataclasses import dataclass, field


from google.genai.types import FunctionCall
from google.genai.types import GroundingMetadata
from google.genai.types import GenerateContentResponse
from google.genai.types import GenerateContentResponseUsageMetadata

from html2text import HTML2Text


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk


log = logging.getLogger(__name__)


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
            yield ModelTextChunk(entry, label="search.sources")

    if search.search_entry_point is not None:
        parser = HTML2Text(bodywidth=0)
        parser.inline_links = False
        parser.protect_links = True
        entry = parser.handle(search.search_entry_point.rendered_content or "")
        yield ModelTextChunk(entry, label="search.suggest")


def _pump_usage(usage: GenerateContentResponseUsageMetadata | None) -> Iterator[StatEvent]:
    if usage is None:
        return

    if usage.prompt_token_count is None:
        usage.prompt_token_count = 0
    yield StatEvent('input', usage.prompt_token_count)

    if usage.cached_content_token_count is None:
        usage.cached_content_token_count = 0
    yield StatEvent('cache_read', usage.cached_content_token_count)

    if usage.candidates_token_count is None:
        usage.candidates_token_count = 0
    yield StatEvent('output', usage.candidates_token_count)


@dataclass
class _PumpFinal:
    usage: GenerateContentResponseUsageMetadata | None = None
    calls: list[FunctionCall] = field(default_factory=list)
    text: str = ""
    search: GroundingMetadata | None = None


def _pump_chunk(chunk: GenerateContentResponse, final: _PumpFinal) -> Iterator[ChatEvent]:
    log.info("%s", chunk.model_dump_json(indent=2))

    if chunk.candidates \
            and chunk.candidates[0].content \
            and chunk.candidates[0].content.parts:

        for part in chunk.candidates[0].content.parts:
            if part.text:
                final.text += part.text
                yield ModelTextChunk(part.text)

            if part.function_call:
                final.calls.append(part.function_call)

        final.usage = chunk.usage_metadata
        final.search = chunk.candidates[0].grounding_metadata


def _pump_calls(calls: list[FunctionCall]) -> Iterator[CallEvent]:
    for call in calls:
        if call.name is None or call.args is None:
            raise ValueError(call.id, call.name, call.args)
        yield CallEvent(call.id or "", call.name, call.args, call.args)


def _pump(streamfun: Callable[[], Iterator[GenerateContentResponse]]) -> Iterator[ChatEvent]:
    stream = streamfun()

    if stream is not None:

        final = _PumpFinal()

        for chunk in stream:
            yield from _pump_chunk(chunk, final)

        yield from _pump_grounding(final.search)

        yield StopEvent(final.text)

        yield from _pump_usage(final.usage)

        yield from _pump_calls(final.calls)
