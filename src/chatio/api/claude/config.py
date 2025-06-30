
from dataclasses import dataclass

from chatio.core.config import ApiConfigFormat
from chatio.core.config import ApiConfigVendor


@dataclass
class ClaudeConfigFormat(ApiConfigFormat):
    use_cache: bool = True


@dataclass
class ClaudeConfigVendor(ApiConfigVendor):
    pass
