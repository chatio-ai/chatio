
from dataclasses import dataclass

from chatio.core.config import ApiTuning
from chatio.core.config import ApiConfig


@dataclass
class ClaudeTuning(ApiTuning):
    use_cache: bool = True


@dataclass
class ClaudeConfig(ApiConfig[ClaudeTuning]):
    pass
