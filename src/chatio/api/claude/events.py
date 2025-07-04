
import logging

from collections.abc import Iterator


from anthropic.lib.streaming import MessageStreamManager


from chatio.core.events import ChatEvent, CallEvent, DoneEvent, StatEvent, TextEvent


log = logging.getLogger(__name__)


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
                if not isinstance(message.input, dict):
                    raise TypeError(message.input)
                yield CallEvent(message.id, message.name, message.input, message.input)
