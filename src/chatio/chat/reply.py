
from collections.abc import Callable
from collections.abc import Iterator

from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk

from chatio.core.stream import ApiStream

from .state import ChatState
from .usage import ChatUsage


# pylint: disable=too-few-public-methods
class ChatReply:

    def __init__(self, model: Callable[[], ApiStream], state: ChatState,
                 calls: Callable[[list[CallEvent]], Iterator[ChatEvent]]) -> None:

        self._model = model
        self._state = state
        self._calls = calls

        self._usage = ChatUsage()

    def __iter__(self) -> Iterator[ChatEvent]:
        calls: list[CallEvent] = []
        stats: list[StatEvent] = []

        events = None
        while not events or calls:
            calls.clear()
            stats.clear()

            stream = self._model()

            with stream as events:
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

            yield from self._usage(stats)

            yield from self._calls(calls)
