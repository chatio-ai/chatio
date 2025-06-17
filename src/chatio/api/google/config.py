
from dataclasses import dataclass

from chatio.core.config import ApiConfigOptions
from chatio.core.config import ApiConfig


@dataclass
class GoogleConfigOptions(ApiConfigOptions):
    grounding: bool = False


@dataclass
class GoogleConfig(ApiConfig[GoogleConfigOptions]):
    pass
