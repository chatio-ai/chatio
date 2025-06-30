
from dataclasses import dataclass

from chatio.core.config import ApiConfigFormat
from chatio.core.config import ApiConfigVendor


@dataclass
class OpenAIConfigFormat(ApiConfigFormat):
    prediction: bool = False
    legacy: bool = False


@dataclass
class OpenAIConfigVendor(ApiConfigVendor):
    pass
