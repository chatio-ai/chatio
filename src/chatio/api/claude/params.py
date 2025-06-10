
from dataclasses import dataclass

from chatio.core.config import ApiParams


@dataclass
class ClaudeParams(ApiParams):
    use_cache: bool = True
