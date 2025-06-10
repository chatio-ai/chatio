
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
