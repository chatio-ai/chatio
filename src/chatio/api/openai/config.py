
from dataclasses import dataclass

from chatio.core.config import ApiFormatConfig
from chatio.core.config import ApiClientConfig


@dataclass
class OpenAIFormatConfig(ApiFormatConfig):
    prediction: bool = False
    compat: bool = False


@dataclass
class OpenAIClientConfig(ApiClientConfig):
    pass
