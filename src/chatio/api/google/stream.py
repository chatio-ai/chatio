
import logging

from collections.abc import AsyncIterator
from collections.abc import Iterator

from collections.abc import Awaitable
from collections.abc import Callable

from dataclasses import dataclass, field

from typing import override


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

from chatio.core.stream import ApiStream


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
    log.debug("%s", chunk.model_dump_json(indent=2))

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


async def _pump(stream: AsyncIterator[GenerateContentResponse]) -> AsyncIterator[ChatEvent]:
    final = _PumpFinal()

    async for chunk in stream:
        for event in _pump_chunk(chunk, final):
            yield event

    for event in _pump_grounding(final.search):
        yield event

    yield StopEvent(final.text)

    for event in _pump_usage(final.usage):
        yield event

    for event in _pump_calls(final.calls):
        yield event


class GoogleStream(ApiStream):

    def __init__(
        self, streamfun: Callable[[], Awaitable[AsyncIterator[GenerateContentResponse]]],
    ) -> None:
        self._streamfun = streamfun

    @override
    # pylint: disable=invalid-overridden-method
    async def __aiter__(self) -> AsyncIterator[ChatEvent]:
        async for event in _pump(await self._streamfun()):
            yield event

    @override
    async def close(self) -> None:
        pass
