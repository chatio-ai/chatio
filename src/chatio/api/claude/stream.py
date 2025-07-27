
import logging

from collections.abc import Iterator

from types import TracebackType

from typing import override


from anthropic.types.usage import Usage
from anthropic.types.content_block import ContentBlock
from anthropic.lib.streaming import MessageStreamEvent
from anthropic.lib.streaming import MessageStreamManager
from anthropic.lib.streaming import MessageStream


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk

from chatio.core.stream import ApiStream


log = logging.getLogger(__name__)


def _pump_usage(usage: Usage | None) -> Iterator[StatEvent]:
    if usage is None:
        return

    if usage.cache_creation_input_tokens is None:
        usage.cache_creation_input_tokens = 0
    if usage.cache_read_input_tokens is None:
        usage.cache_read_input_tokens = 0

    usage.input_tokens += usage.cache_creation_input_tokens
    usage.input_tokens += usage.cache_read_input_tokens
    yield StatEvent('input', usage.input_tokens)
    yield StatEvent('cache_written', usage.cache_creation_input_tokens)
    yield StatEvent('cache_read', usage.cache_read_input_tokens)
    yield StatEvent('output', usage.output_tokens)


def _pump_chunk(chunk: MessageStreamEvent) -> Iterator[ChatEvent]:
    log.debug("%s", chunk.model_dump_json(indent=2))

    if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
        yield ModelTextChunk(chunk.delta.text)
    if chunk.type == 'content_block_stop' and chunk.content_block.type == 'text' \
            and chunk.content_block.citations is not None:
        for citation in chunk.content_block.citations:
            yield ModelTextChunk(citation.cited_text, label="claude.citation")


def _pump_calls(content: list[ContentBlock]) -> Iterator[CallEvent]:
    for message in content:
        if message.type == 'tool_use':
            if not isinstance(message.input, dict):
                raise TypeError(message.input)
            yield CallEvent(message.id, message.name, message.input, message.input)


def _pump(stream: MessageStream) -> Iterator[ChatEvent]:
    for chunk in stream:
        yield from _pump_chunk(chunk)

    final = stream.get_final_message()

    final_content = "".join(block.text for block in final.content if block.type == 'text')
    yield StopEvent(final_content)

    yield from _pump_usage(final.usage)

    yield from _pump_calls(final.content)


class ClaudeStream(ApiStream):

    def __init__(self, streamctx: MessageStreamManager) -> None:
        self._streamctx = streamctx

    @override
    def __enter__(self) -> Iterator[ChatEvent]:
        stream = self._streamctx.__enter__()
        return _pump(stream)

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return self._streamctx.__exit__(exc_type, exc, exc_tb)
