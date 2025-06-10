
from dataclasses import dataclass

from chatio.core.config import ApiParams


@dataclass
class GoogleParams(ApiParams):
    grounding: bool = False
