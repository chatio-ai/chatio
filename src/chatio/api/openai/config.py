
from dataclasses import dataclass

from chatio.core.config import ApiTuning
from chatio.core.config import ApiConfig


@dataclass
class OpenAITuning(ApiTuning):
    prediction: bool = False
    legacy: bool = False


@dataclass
class OpenAIConfig(ApiConfig[OpenAITuning]):
    pass
