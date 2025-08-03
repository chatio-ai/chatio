
from collections.abc import Callable
from collections.abc import Iterator

from types import TracebackType

from typing import Self

from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent

from chatio.core.stream import ApiStream

from .state import ChatState
from .usage import ChatUsage


class ChatReply:

    def __init__(self, model: Callable[[], ApiStream], state: ChatState,
                 calls: Callable[[list[CallEvent], ChatState], Iterator[ChatEvent]]) -> None:

        self._model = model
        self._state = state
        self._calls = calls

        self._ready = False

        self._usage = ChatUsage()

        self._stream: ApiStream | None = None

    def __enter__(self) -> Self:
        if self._stream is not None:
            raise RuntimeError
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None

    def __iter__(self) -> Iterator[ChatEvent]:
        while not self._ready:
            calls: list[CallEvent] = []
            stats: list[StatEvent] = []

            self._stream = self._model()

            for event in self._stream:
                match event:
                    case StopEvent(text):
                        if text:
                            self._state.append_output_message(text)
                        yield event
                    case CallEvent():
                        calls.append(event)
                    case StatEvent():
                        stats.append(event)
                    case _:
                        yield event

            self._stream.close()

            yield from self._usage(stats)

            yield from self._calls(calls, self._state)

            self._ready = not calls
