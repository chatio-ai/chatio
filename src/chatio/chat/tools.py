
from dataclasses import dataclass, field

from collections.abc import Iterator
from collections.abc import Callable

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools as _ChatTools

from toolbelt import ToolBase


@dataclass
class ChatTools(_ChatTools):
    funcs: dict[str, Callable[..., Iterator[str | dict]]] = field(default_factory=dict)

    def __init__(self, tools: list[ToolBase] | None = None,
                 tool_choice_mode: str | None = None, tool_choice_name: str | None = None) -> None:

        if tools is None:
            tools = []

        _tools = []
        _funcs = {}
        for tool in tools:
            schema = tool.schema()
            name = schema.pop("name")
            desc = schema.pop("description")

            if not name or not desc or not schema:
                raise RuntimeError

            _funcs[name] = tool.__call__
            _tools.append(ToolSchema(name, desc, schema))

        if tool_choice_name and tool_choice_name not in tools:
            raise ValueError
        _tool_choice = ToolChoice(tool_choice_mode, tool_choice_name)

        super().__init__(_tools, _tool_choice)
        self.funcs = _funcs
