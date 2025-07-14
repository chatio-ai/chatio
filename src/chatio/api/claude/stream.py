
import logging

from collections.abc import AsyncIterator
from collections.abc import Iterator

from typing import override


from anthropic.types.usage import Usage
from anthropic.types.content_block import ContentBlock
from anthropic.lib.streaming import MessageStreamEvent
from anthropic.lib.streaming import AsyncMessageStreamManager
from anthropic.lib.streaming import AsyncMessageStream


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


async def _pump(stream: AsyncMessageStream) -> AsyncIterator[ChatEvent]:
    async for chunk in stream:
        for event in _pump_chunk(chunk):
            yield event

    final = await stream.get_final_message()

    final_content = "".join(block.text for block in final.content if block.type == 'text')
    yield StopEvent(final_content)

    for event in _pump_usage(final.usage):
        yield event

    for event in _pump_calls(final.content):
        yield event


class ClaudeStream(ApiStream):

    def __init__(self, streamctx: AsyncMessageStreamManager) -> None:
        self._streamctx = streamctx

    @override
    # pylint: disable=invalid-overridden-method
    async def __aiter__(self) -> AsyncIterator[ChatEvent]:
        stream = await self._streamctx.__aenter__()
        async for event in _pump(stream):
            yield event

    @override
    async def close(self) -> None:
        return await self._streamctx.__aexit__(None, None, None)
