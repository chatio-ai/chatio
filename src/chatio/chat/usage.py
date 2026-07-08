
from collections.abc import Iterator

from chatio.core.events import StatEvent


class ChatUsage:

    def __init__(self) -> None:
        self._stats: dict[str, int] = {}
        self._input = 0

    def __call__(self, usage: list[StatEvent]) -> Iterator[StatEvent]:
        return self.generate(usage)

    def _emit_event(self, label: str, delta: int) -> StatEvent:
        total = self._stats.setdefault(label, 0) + delta
        self._stats[label] = total

        return StatEvent(label, delta, total)

    def generate(self, events: list[StatEvent]) -> Iterator[StatEvent]:
        values = {}
        for event in events:
            values[event.label] = event.delta
            yield self._emit_event(event.label, event.delta)

        input_ = values.get('input')
        if input_ is None:
            return

        yield self._emit_event('input_real', input_ - self._input)

        self._input = input_

        cache_read = values.get('cache_read')
        if cache_read is None:
            return

        cache_written = values.get('cache_written', 0)

        yield self._emit_event('cache_miss', input_ - cache_written - cache_read)
