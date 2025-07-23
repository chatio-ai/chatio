
import os


from chatio.chat.tools import ChatTools
from chatio.chat import Chat

from chatio.tool.shell import ShellCalcTool
from chatio.tool.shell import ShellExecTool
from chatio.tool.dummy import DoNothingTool

from chatio.tool.wiki import WikiToolFactory
from chatio.tool.web import WebSearchTool
from chatio.tool.web import WebBrowseTool

from chatio.tool.image import ImageDumpTool

from chatio.tool.llm import LlmDialogTool


from .model import build_model


def build_tools(tools_name: str | None = None, env_ns: str | None = None) -> ChatTools:
    _env_ns = "CHATIO"
    if env_ns is not None:
        _env_ns = _env_ns + "_" + env_ns

    if tools_name is None:
        env_name = f"{_env_ns}_TOOLS_NAME"
        tools_name = os.environ.get(env_name)
        if not tools_name:
            tools_name = 'empty'

    tools_name, _, tool_choice = tools_name.partition(':')
    tool_choice_mode, _, tool_choice_name = tool_choice.partition(':')

    tools: list | None = None
    match tools_name:
        case 'default':
            wiki = WikiToolFactory()

            tools = [
                ShellExecTool(),
                ShellCalcTool(),
                wiki.wiki_content(),
                wiki.wiki_summary(),
                wiki.wiki_section(),
                wiki.wiki_search(),
                WebSearchTool(),
                WebBrowseTool(),
                DoNothingTool(),
            ]
        case 'llmtool':
            llm = build_llm_tool()
            tools = [
                LlmDialogTool(llm),
            ]
        case 'imgtool':
            tools = [
                ImageDumpTool(),
            ]

    return ChatTools(tools, tool_choice_mode, tool_choice_name)


def build_llm_tool() -> Chat:
    _env_ns = "NESTED"

    _model = build_model(env_ns=_env_ns)
    _tools = build_tools(env_ns=_env_ns)

    return Chat(model=_model, tools=_tools)
