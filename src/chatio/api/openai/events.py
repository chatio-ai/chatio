
import logging

from collections.abc import Iterator


from openai.types.completion_usage import CompletionUsage
from openai.types.chat.parsed_function_tool_call import ParsedFunctionToolCall
from openai.lib.streaming.chat._events import ChatCompletionStreamEvent
from openai.lib.streaming.chat._completions import ChatCompletionStreamManager


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk


log = logging.getLogger(__name__)


def _pump_usage(usage: CompletionUsage | None) -> Iterator[StatEvent]:
    if usage is None:
        return

    yield StatEvent('input', usage.prompt_tokens)

    input_details = usage.prompt_tokens_details
    if input_details is not None:
        if input_details.cached_tokens is None:
            input_details.cached_tokens = 0
        yield StatEvent('cache_read', input_details.cached_tokens)

    yield StatEvent('output', usage.completion_tokens)

    output_details = usage.completion_tokens_details
    if output_details is not None:
        if output_details.accepted_prediction_tokens is not None:
            yield StatEvent('prediction_accept', output_details.accepted_prediction_tokens)
        if output_details.rejected_prediction_tokens is not None:
            yield StatEvent('prediction_reject', output_details.rejected_prediction_tokens)


def _pump_chunk(chunk: ChatCompletionStreamEvent) -> Iterator[ChatEvent]:
    log.debug("%s", chunk.model_dump_json(indent=2))

    if chunk.type == 'content.delta':
        yield ModelTextChunk(chunk.delta)


def _pump_calls(calls: list[ParsedFunctionToolCall] | None) -> Iterator[CallEvent]:
    if calls is None:
        return

    for call in calls:
        if not isinstance(call.function.parsed_arguments, dict):
            raise TypeError(call.function.parsed_arguments)
        yield CallEvent(call.id, call.function.name,
                        call.function.parsed_arguments, call.function.arguments)


def _pump(streamctx: ChatCompletionStreamManager) -> Iterator[ChatEvent]:
    with streamctx as stream:
        for chunk in stream:
            yield from _pump_chunk(chunk)

        final = stream.get_final_completion()
        final_message = final.choices[0].message
        yield StopEvent(final_message.content or "")

        yield from _pump_usage(final.usage)

        yield from _pump_calls(final_message.tool_calls)
