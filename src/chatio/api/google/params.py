
from dataclasses import dataclass

from google.genai.types import ContentDict

from chatio.core.params import ApiStateOptions


@dataclass
class GoogleStateOptions(ApiStateOptions):
    system: ContentDict | None = None
