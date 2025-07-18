
from collections.abc import AsyncIterator
from collections.abc import Callable

from typing import override

from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent

from chatio.core.stream import ApiStream

from .state import ChatState
from .tools import ChatTools
from .usage import ChatUsage


class ChatReply(ApiStream):

    def __init__(self, model: Callable[[ChatState, ChatTools], ApiStream],
                 state: ChatState, tools: ChatTools) -> None:

        self._model = model
        self._state = state
        self._tools = tools

        self._ready = False

        self._usage = ChatUsage()

        self._stream: ApiStream | None = None

    @override
    async def close(self) -> None:
        if self._stream is not None:
            await self._stream.close()
            self._stream = None

    @override
    # pylint: disable=invalid-overridden-method
    async def __aiter__(self) -> AsyncIterator[ChatEvent]:
        while not self._ready:
            calls: list[CallEvent] = []
            stats: list[StatEvent] = []

            self._stream = self._model(self._state, self._tools)

            async for event in self._stream:
                match event:
                    case CallEvent():
                        calls.append(event)
                    case StatEvent():
                        stats.append(event)
                    case StopEvent(text):
                        self._state.append_output_message(text)
                        yield event
                    case _:
                        yield event

            await self._stream.close()

            for event in self._usage(stats):
                yield event

            async for event in self._tools(calls, self._state):
                yield event

            self._ready = not calls
