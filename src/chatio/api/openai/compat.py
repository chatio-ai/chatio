
from collections.abc import AsyncIterator
from collections.abc import Callable

from typing import override

from openai.types.chat.chat_completion_chunk import ChoiceDelta
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from openai._models import FinalRequestOptions
from openai import AsyncOpenAI
from openai import AsyncStream
from openai import NotGiven


# pylint: disable=too-few-public-methods
class _AsyncStream(AsyncStream[ChatCompletionChunk]):
    def __init__(self, client: AsyncOpenAI, stream: AsyncStream[ChatCompletionChunk]) -> None:
        super().__init__(cast_to=ChatCompletionChunk, response=stream.response, client=client)
        self._tool_call_index = -1

    def _patch_chat_completion_chunk(self, chunk: ChatCompletionChunk) -> None:
        chunk.object = 'chat.completion.chunk'

        if chunk.choices is None:
            chunk.choices = []

        for choice in chunk.choices:
            if choice.delta is None:
                choice.delta = ChoiceDelta()
            if not isinstance(choice.delta.content, str):
                choice.delta.content = None
            if choice.delta.tool_calls is not None:
                for tool_call in choice.delta.tool_calls:
                    if not tool_call.type:
                        tool_call.index = self._tool_call_index
                        tool_call.type = 'function'
                    else:
                        self._tool_call_index += 1
                        tool_call.index = self._tool_call_index

    async def __stream__(self) -> AsyncIterator[ChatCompletionChunk]:
        async for chunk in super().__stream__():
            self._patch_chat_completion_chunk(chunk)
            yield chunk


# pylint: disable=too-few-public-methods
class _ChunkParser:
    def __init__(self, client: AsyncOpenAI, parser: Callable | NotGiven) -> None:
        self._client = client
        self._parser = parser

    def __call__(self, result: object) -> object:
        if isinstance(result, AsyncStream):
            method = result.response.request.headers.get('x-stainless-helper-method')
            if method == 'chat.completions.stream':
                result = _AsyncStream(self._client, result)

        if isinstance(self._parser, NotGiven):
            return result

        return self._parser(result)


class AsyncCompat(AsyncOpenAI):
    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        options = await super()._prepare_options(options)
        options.post_parser = _ChunkParser(self, options.post_parser)
        return options
