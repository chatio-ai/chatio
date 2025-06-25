
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.params import ApiParams


@dataclass
class GoogleParams(ApiParams[
    ContentDict,
    ContentDict,
    ToolListUnionDict,
    ToolConfigDict,
    None,
]):
    pass
