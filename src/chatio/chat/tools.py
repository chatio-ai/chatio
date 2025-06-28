
from dataclasses import dataclass, field

from collections.abc import Callable

from chatio.core.config import ToolsConfig

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools as _ChatTools


@dataclass
class ChatTools(_ChatTools):
    funcs: dict[str, Callable] = field(default_factory=dict)


def build_tools(tools: ToolsConfig | None = None) -> ChatTools:
    if tools is None:
        return ChatTools()

    if tools.tools is None:
        tools.tools = {}

    _funcs = {}
    _tools = []
    for name, tool in tools.tools.items():
        desc = tool.desc()
        schema = tool.schema()

        if not name or not desc or not schema:
            raise RuntimeError

        _funcs[name] = tool

        _tools.append(ToolSchema(name, desc, schema))

    _tool_choice = ToolChoice(tools.tool_choice_mode, tools.tool_choice_name, list(tools.tools))

    return ChatTools(
        funcs=_funcs,
        tools=_tools,
        tool_choice=_tool_choice,
    )
