
from dataclasses import dataclass


@dataclass
class ChatStatInputData:
    input_tokens: int = 0
    input_history_tokens: int = 0
    input_current_tokens: int = 0


@dataclass
class ChatStatOutputData:
    output_tokens: int = 0
    predict_accepted: int = 0
    predict_rejected: int = 0


@dataclass
class ChatStatCacheData:
    cache_missed: int = 0
    cache_written: int = 0
    cache_read: int = 0


@dataclass
class ChatStatData:
    input: ChatStatInputData
    output: ChatStatOutputData
    cache: ChatStatCacheData

    def __init__(self, label):
        self.input = ChatStatInputData()
        self.output = ChatStatOutputData()
        self.cache = ChatStatCacheData()
        self.label = label


@dataclass
class ChatStat:
    _round: ChatStatData
    _total: ChatStatData

    def __init__(self):
        self._round = ChatStatData("round")
        self._total = ChatStatData("total")

    def __call__(self, usage):
        return self._process(usage)

    def _mkevent(self, stats):
        return {
            "type": "token_stats",
            "scope": stats.label,
            "input_tokens": stats.input.input_tokens,
            "input_history_tokens": stats.input.input_history_tokens,
            "input_current_tokens": stats.input.input_current_tokens,
            "output_tokens": stats.output.output_tokens,
            "cache_missed": stats.cache.cache_missed,
            "cache_written": stats.cache.cache_written,
            "cache_read": stats.cache.cache_read,
            "predict_accepted": stats.output.predict_accepted,
            "predict_rejected": stats.output.predict_rejected,
        }

    def _process(self, usage):
        self._round.input.input_history_tokens = self._round.input.input_tokens
        self._round.input.input_current_tokens = usage.input_tokens - self._round.input.input_history_tokens
        self._round.input.input_tokens = usage.input_tokens
        self._round.output.output_tokens = usage.output_tokens

        self._round.cache.cache_missed = usage.input_tokens - usage.cache_written - usage.cache_read
        self._round.cache.cache_written = usage.cache_written
        self._round.cache.cache_read = usage.cache_read

        self._round.output.predict_accepted = usage.predict_accepted
        self._round.output.predict_rejected = usage.predict_rejected

        yield self._mkevent(self._round)

        self._total.input.input_history_tokens += self._round.input.input_history_tokens
        self._total.input.input_current_tokens += self._round.input.input_current_tokens
        self._total.input.input_tokens += self._round.input.input_tokens
        self._total.output.output_tokens += self._round.output.output_tokens

        self._total.cache.cache_missed += self._round.cache.cache_missed
        self._total.cache.cache_written += self._round.cache.cache_written
        self._total.cache.cache_read += self._round.cache.cache_read

        self._total.output.predict_accepted += self._round.output.predict_accepted
        self._total.output.predict_rejected += self._round.output.predict_rejected

        yield self._mkevent(self._total)
