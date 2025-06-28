
from dataclasses import dataclass

from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict

from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict

from chatio.core.params import ApiStateOptions
from chatio.core.params import ApiParams


@dataclass
class GoogleStateOptions(ApiStateOptions):
    system: ContentDict | None = None


@dataclass
class GoogleParams(ApiParams):
    max_output_tokens: int

    messages: list[ContentUnionDict]

    system_instruction: ContentDict | None = None

    tools: ToolListUnionDict | None = None

    tool_config: ToolConfigDict | None = None
