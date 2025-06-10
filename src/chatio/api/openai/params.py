
from dataclasses import dataclass

from chatio.api._common import ApiParams


@dataclass
class OpenAIParams(ApiParams):
    prediction: bool = False
    legacy: bool = False
