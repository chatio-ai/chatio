
from dataclasses import dataclass

from chatio.core.config import ApiConfigFormat
from chatio.core.config import ApiConfigClient


@dataclass
class ClaudeConfigFormat(ApiConfigFormat):
    use_cache: bool = True


@dataclass
class ClaudeConfigClient(ApiConfigClient):
    pass
