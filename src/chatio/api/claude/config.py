
from dataclasses import dataclass

from chatio.core.config import ApiFormatConfig
from chatio.core.config import ApiClientConfig


@dataclass
class ClaudeFormatConfig(ApiFormatConfig):
    use_cache: bool = True


@dataclass
class ClaudeClientConfig(ApiClientConfig):
    pass
