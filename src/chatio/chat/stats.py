
from dataclasses import dataclass


@dataclass
class ChatStatData:
    input_tokens: int = 0
    input_history_tokens: int = 0
    input_current_tokens: int = 0
    output_tokens: int = 0
    cache_missed: int = 0
    cache_written: int = 0
    cache_read: int = 0

    def __init__(self, label):
        self.label = label


class ChatStat:
    def __init__(self):
        self._round = ChatStatData("round")
        self._total = ChatStatData("total")

    def __call__(self, usage):
        return self._process(usage)

    def _mkevent(self, stats):
        return {
            "type": "token_stats",
            "scope": stats.label,
            "input_tokens": stats.input_tokens,
            "input_history_tokens": stats.input_history_tokens,
            "input_current_tokens": stats.input_current_tokens,
            "output_tokens": stats.output_tokens,
            "cache_missed": stats.cache_missed,
            "cache_written": stats.cache_written,
            "cache_read": stats.cache_read,
        }

    def _process(self, usage):
        self._round.input_history_tokens = self._round.input_tokens
        self._round.input_current_tokens = usage.input_tokens - self._round.input_history_tokens
        self._round.input_tokens = usage.input_tokens
        self._round.output_tokens = usage.output_tokens

        self._round.cache_missed = usage.input_tokens - usage.cache_written - usage.cache_read
        self._round.cache_written = usage.cache_written
        self._round.cache_read = usage.cache_read

        yield self._mkevent(self._round)

        self._total.input_history_tokens += self._round.input_history_tokens
        self._total.input_current_tokens += self._round.input_current_tokens
        self._total.input_tokens += self._round.input_tokens
        self._total.output_tokens += self._round.output_tokens

        self._total.cache_missed += self._round.cache_missed
        self._total.cache_written += self._round.cache_written
        self._total.cache_read += self._round.cache_read

        yield self._mkevent(self._total)
