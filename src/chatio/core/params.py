
from collections.abc import Callable

from dataclasses import dataclass, field


from .models import SystemMessage
from .models import ContentEntry
from .models import ToolSchema
from .models import ToolChoice
from .models import PredictMessage


@dataclass
class ApiParamsBase[
    SystemContentT,
    MessageContentT,
    ToolDefinitionsT,
    ToolSelectionT,
    ChatPredictionT,
]:
    system: SystemContentT | None = None
    messages: list[MessageContentT] = field(default_factory=list)
    predict: ChatPredictionT | None = None
    tools: ToolDefinitionsT | None = None
    tool_choice: ToolSelectionT | None = None


@dataclass
class ApiParams(ApiParamsBase[
    SystemMessage,
    ContentEntry,
    list[ToolSchema],
    ToolChoice,
    PredictMessage,
]):
    extras: dict[str, ContentEntry | None] = field(default_factory=dict)
    funcs: dict[str, Callable] = field(default_factory=dict)
