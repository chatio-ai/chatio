
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.params import ApiParamsBase


@dataclass
class GoogleParams(ApiParamsBase[
    ContentDict,
    ContentUnionDict,
    ToolListUnionDict,
    ToolConfigDict,
    None,
]):
    pass
