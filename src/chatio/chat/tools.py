
from dataclasses import dataclass, field

from collections.abc import Callable

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools as _ChatTools


@dataclass
class ChatTools(_ChatTools):
    funcs: dict[str, Callable] = field(default_factory=dict)

    def __init__(self, tools: dict | None = None,
                 tool_choice_mode: str | None = None, tool_choice_name: str | None = None) -> None:

        if tools is None:
            tools = {}

        _tools = []
        _funcs = {}
        for name, tool in tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            _funcs[name] = tool
            _tools.append(ToolSchema(name, desc, schema))

        if tool_choice_name and tool_choice_name not in tools:
            raise ValueError
        _tool_choice = ToolChoice(tool_choice_mode, tool_choice_name)

        super().__init__(_tools, _tool_choice)
        self.funcs = _funcs
