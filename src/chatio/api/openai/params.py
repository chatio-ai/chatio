
from dataclasses import dataclass

from chatio.core.config import ApiParams


@dataclass
class OpenAIParams(ApiParams):
    prediction: bool = False
    legacy: bool = False
