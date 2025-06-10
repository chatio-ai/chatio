
from dataclasses import dataclass

from chatio.api._common import ApiParams


@dataclass
class ClaudeParams(ApiParams):
    use_cache: bool = True
