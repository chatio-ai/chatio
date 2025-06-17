
from dataclasses import dataclass

from chatio.core.config import ApiConfig
from chatio.core.config import ApiTuning


@dataclass
class GoogleTuning(ApiTuning):
    grounding: bool = False


@dataclass
class GoogleConfig(ApiConfig[GoogleTuning]):
    pass
