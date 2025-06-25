
from collections.abc import Callable

from dataclasses import dataclass, field


from .models import SystemMessage
from .models import ContentEntry
from .models import ToolSchema
from .models import ToolChoice
from .models import PredictMessage


@dataclass
class ApiParamsBase[
    SystemContent,
    MessageContent,
    ToolDefinitions,
    ToolSelection,
    ChatPrediction,
]:
    system: SystemContent | None = None
    messages: list[MessageContent] = field(default_factory=list)
    predict: ChatPrediction | None = None
    tools: ToolDefinitions | None = None
    tool_choice: ToolSelection | None = None


@dataclass
class ApiParams(ApiParamsBase[
    SystemMessage,
    ContentEntry,
    list[ToolSchema],
    ToolChoice,
    PredictMessage,
]):
    funcs: dict[str, Callable] = field(default_factory=dict)
