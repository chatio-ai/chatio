
from collections.abc import Iterator

from chatio.core.events import StatEvent


class ChatUsage:

    def __init__(self):
        self._stats: dict[str, int] = {}

    def __call__(self, usage) -> Iterator[dict]:
        return self.generate(usage)

    def generate(self, event: StatEvent) -> Iterator[dict]:
        total = self._stats.setdefault(event.label, 0) + event.delta
        self._stats[event.label] = total

        yield {
            'type': 'token_usage',
            'label': event.label,
            'delta': event.delta,
            'total': total,
        }

        # self._delta.input.input_history_tokens = self._delta.input.input_tokens
        # self._delta.input.input_current_tokens = usage.input_tokens - self._delta.input.input_history_tokens

        # self._delta.cache.cache_missed = usage.input_tokens - usage.cache_written - usage.cache_read
