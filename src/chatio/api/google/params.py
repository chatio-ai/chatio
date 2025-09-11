
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict

from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict

from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParamsImpl


@dataclass
class GoogleStateOptions(ApiStateOptions):
    system: ContentDict | None = None


@dataclass
class GoogleParams(ApiParamsImpl[
    ContentUnionDict,
    GoogleStateOptions,
    ToolListUnionDict | None,
    ToolConfigDict | None,
]):
    pass
