
from dataclasses import dataclass

from chatio.core.config import ApiConfigOptions
from chatio.core.config import ApiConfig


@dataclass
class OpenAIConfigOptions(ApiConfigOptions):
    prediction: bool = False
    legacy: bool = False


@dataclass
class OpenAIConfig(ApiConfig[OpenAIConfigOptions]):
    pass
