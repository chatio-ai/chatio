
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict

from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


@dataclass
class GoogleParams:
    messages: list[ContentUnionDict]
    system: ContentDict | None = None
    tools: ToolListUnionDict | None = None
    tool_config: ToolConfigDict | None = None
