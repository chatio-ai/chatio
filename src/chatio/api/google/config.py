
from dataclasses import dataclass

from chatio.core.config import ApiConfigFormat
from chatio.core.config import ApiConfigClient


@dataclass
class GoogleConfigFormat(ApiConfigFormat):
    grounding: bool = False


@dataclass
class GoogleConfigClient(ApiConfigClient):
    pass
