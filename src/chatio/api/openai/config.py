
from dataclasses import dataclass

from chatio.core.config import ApiConfigFormat
from chatio.core.config import ApiConfigClient


@dataclass
class OpenAIConfigFormat(ApiConfigFormat):
    prediction: bool = False
    compat: bool = False


@dataclass
class OpenAIConfigClient(ApiConfigClient):
    pass
