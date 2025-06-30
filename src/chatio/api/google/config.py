
from dataclasses import dataclass

from chatio.core.config import ApiConfigFormat
from chatio.core.config import ApiConfigVendor


@dataclass
class GoogleConfigFormat(ApiConfigFormat):
    grounding: bool = False


@dataclass
class GoogleConfigVendor(ApiConfigVendor):
    pass
