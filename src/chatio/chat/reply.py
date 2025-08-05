
from collections.abc import Callable
from collections.abc import Iterator

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
    def close(self) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None

    @override
    def __iter__(self) -> Iterator[ChatEvent]:
        while not self._ready:
            calls: list[CallEvent] = []
            stats: list[StatEvent] = []

            self._stream = self._model(self._state, self._tools)

            for event in self._stream:
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

            self._stream.close()

            yield from self._usage(stats)

            yield from self._tools(calls, self._state)

            self._ready = not calls
