
from dataclasses import dataclass


@dataclass
class ChatStatData:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_written: int = 0
    cache_read: int = 0


class ChatStat:
    def __init__(self):
        self._stats = ChatStatData()

    def __call__(self, usage):
        return self._process(usage)

    def _process(self, usage):
        yield {
            "type": "token_stats",
            "scope": "round",
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cache_written": usage.cache_written,
            "cache_read": usage.cache_read,
        }

        self._stats.input_tokens += usage.input_tokens
        self._stats.output_tokens += usage.output_tokens
        self._stats.cache_written += usage.cache_written
        self._stats.cache_read += usage.cache_read

        yield {
            "type": "token_stats",
            "scope": "total",
            "input_tokens": self._stats.input_tokens,
            "output_tokens": self._stats.output_tokens,
            "cache_written": self._stats.cache_written,
            "cache_read": self._stats.cache_read,
        }
