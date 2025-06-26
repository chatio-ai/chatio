
from chatio.core.config import ToolsConfig

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools


def build_tools(tools: ToolsConfig | None = None) -> ChatTools:
    _tools = ChatTools()

    if tools is None:
        return _tools

    if tools.tools is None:
        tools.tools = {}

    _tools.tools = []
    for name, tool in tools.tools.items():
        desc = tool.desc()
        schema = tool.schema()

        if not name or not desc or not schema:
            raise RuntimeError

        _tools.funcs[name] = tool

        _tools.tools.append(ToolSchema(name, desc, schema))

    _tools.tool_choice = ToolChoice(
        tools.tool_choice_mode, tools.tool_choice_name, list(tools.tools))

    return _tools
