
from dataclasses import dataclass

from chatio.core.config import ApiConfigOptions
from chatio.core.config import ApiConfig


@dataclass
class ClaudeConfigOptions(ApiConfigOptions):
    use_cache: bool = True


@dataclass
class ClaudeConfig(ApiConfig[ClaudeConfigOptions]):
    pass
