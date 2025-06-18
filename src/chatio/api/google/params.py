
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.params import ApiParams


@dataclass(init=False)
class GoogleParams(ApiParams[
    ContentDict,
    ContentDict,
    None,
    ToolListUnionDict,
    ToolConfigDict,
]):
    pass
