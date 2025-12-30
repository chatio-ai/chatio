
import logging

from collections.abc import AsyncIterator
from collections.abc import Iterator

from typing import override


from openai.types.completion_usage import CompletionUsage
from openai.types.chat import ChatCompletion
from openai.types.chat.parsed_function_tool_call import ParsedFunctionToolCall
from openai.lib.streaming.chat._events import ChatCompletionStreamEvent
from openai.lib.streaming.chat._completions import AsyncChatCompletionStreamManager
from openai.lib.streaming.chat._completions import AsyncChatCompletionStream

from openai import LengthFinishReasonError


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk

from chatio.core.stream import ApiStream


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


def _pump_compl(completion: ChatCompletion) -> Iterator[ChatEvent]:
    message = completion.choices[0].message
    if message.content is None:
        message.content = ""
    yield StopEvent(message.content)

    yield from _pump_usage(completion.usage)


async def _pump(stream: AsyncChatCompletionStream) -> AsyncIterator[ChatEvent]:
    async for chunk in stream:
        for event in _pump_chunk(chunk):
            yield event

    try:
        final = await stream.get_final_completion()
        for event in _pump_compl(final):
            yield event

        for event in _pump_calls(final.choices[0].message.tool_calls):
            yield event
    except LengthFinishReasonError as e:
        for event in _pump_compl(e.completion):
            yield event


class OpenAIStream(ApiStream):

    def __init__(self, streamctx: AsyncChatCompletionStreamManager) -> None:
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
