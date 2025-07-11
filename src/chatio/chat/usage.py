
from collections.abc import Iterator

from chatio.core.events import StatEvent


class ChatUsage:

    def __init__(self):
        self._stats: dict[str, int] = {}
        self._input = 0

    def __call__(self, usage) -> Iterator[StatEvent]:
        return self.generate(usage)

    def _emit_event(self, label: str, delta: int) -> StatEvent:
        total = self._stats.setdefault(label, 0) + delta
        self._stats[label] = total

        return StatEvent(label, delta, total)

    def generate(self, events: list[StatEvent]) -> Iterator[StatEvent]:
        _values = {}
        for event in events:
            _values[event.label] = event.delta
            yield self._emit_event(event.label, event.delta)

        _input = _values.get('input', 0)
        yield self._emit_event('input_real', _input - self._input)

        self._input = _input

        _cache_written = _values.get('cache_written', 0)
        _cache_read = _values.get('cache_read', 0)

        yield self._emit_event('cache_miss', _input - _cache_written - _cache_read)
