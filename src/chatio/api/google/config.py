
from dataclasses import dataclass

from chatio.core.config import ApiFormatConfig
from chatio.core.config import ApiClientConfig


@dataclass
class GoogleFormatConfig(ApiFormatConfig):
    grounding: bool = False


@dataclass
class GoogleClientConfig(ApiClientConfig):
    pass
