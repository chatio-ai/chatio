
from collections.abc import Callable
from collections.abc import Iterator

from types import TracebackType

from typing import Self

from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk

from chatio.core.stream import ApiStream

from .state import ChatState
from .usage import ChatUsage


class ChatReply:

    def __init__(self, model: Callable[[], ApiStream], state: ChatState,
                 calls: Callable[[list[CallEvent]], Iterator[ChatEvent]]) -> None:

        self._model = model
        self._state = state
        self._calls = calls

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
        if self._stream is not None:
            self._stream.__exit__(exc_type, exc_value, traceback)
            self._stream = None

    def __iter__(self) -> Iterator[ChatEvent]:
        calls: list[CallEvent] = []
        stats: list[StatEvent] = []

        while True:
            calls.clear()
            stats.clear()

            self._stream = self._model()
            events = self._stream.__enter__()

            for event in events:
                match event:
                    case ModelTextChunk():
                        yield event
                    case StopEvent(text):
                        if text:
                            self._state.append_output_message(text)
                    case CallEvent():
                        calls.append(event)
                    case StatEvent():
                        stats.append(event)

            self._stream.__exit__(None, None, None)
            self._stream = None

            yield from self._usage(stats)

            yield from self._calls(calls)

            if not calls:
                break
