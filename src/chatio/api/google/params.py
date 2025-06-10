
from dataclasses import dataclass

from chatio.api._common import ApiParams


@dataclass
class GoogleParams(ApiParams):
    grounding: bool = False
