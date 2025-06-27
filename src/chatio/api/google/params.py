
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict

from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict

from chatio.core.params import ApiParams


@dataclass
class GoogleParams(ApiParams):

    messages: list[ContentUnionDict]

    system: ContentDict | None = None

    tools: ToolListUnionDict | None = None

    tool_config: ToolConfigDict | None = None
