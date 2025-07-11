
import logging

from collections.abc import Iterator


from anthropic.types.usage import Usage
from anthropic.lib.streaming import MessageStreamManager


from chatio.core.events import ChatEvent, CallEvent, DoneEvent, StatEvent, TextEvent


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
    yield StatEvent('output', usage.output_tokens)
    yield StatEvent('cache_written', usage.cache_creation_input_tokens)
    yield StatEvent('cache_read', usage.cache_read_input_tokens)


def _pump(streamctx: MessageStreamManager) -> Iterator[ChatEvent]:
    with streamctx as stream:
        for chunk in stream:
            log.info("%s", chunk.model_dump_json(indent=2))

            if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                yield TextEvent(chunk.delta.text)
            if chunk.type == 'content_block_stop' and chunk.content_block.type == 'text' \
                    and chunk.content_block.citations is not None:
                for citation in chunk.content_block.citations:
                    yield TextEvent(citation.cited_text, label="claude.citation")

        final = stream.get_final_message()

        final_content = "".join(block.text for block in final.content if block.type == 'text')
        yield DoneEvent(final_content)

        yield from _pump_usage(final.usage)

        for message in final.content:
            if message.type == 'tool_use':
                if not isinstance(message.input, dict):
                    raise TypeError(message.input)
                yield CallEvent(message.id, message.name, message.input, message.input)
