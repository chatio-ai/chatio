
import os


from chatio.core.invoke import ToolBase
from chatio.chat.tools import ChatTools
from chatio.chat import Chat

from chatio.tool.shell import ShellCalcTool
from chatio.tool.shell import ShellExecTool
from chatio.tool.dummy import DoNothingTool

from chatio.tool.wiki import WikiToolFactory
from chatio.tool.web import DuckDuckGoTool as WebSearchTool
from chatio.tool.web import WebBrowseTool

from chatio.tool.image import ImageDumpTool

from chatio.tool.llm import LlmDialogTool


from .model import build_model


def _build_tools_name(tools_name: str | None = None, env_ns: str = "") -> list[ToolBase] | None:
    env_ns = f"CHATIO_{env_ns}" if env_ns else "CHATIO"
    if tools_name is None:
        env_name = f"{env_ns}_TOOLS_NAME"
        tools_name = os.environ.get(env_name)
        if not tools_name:
            tools_name = 'empty'

    tools_name, _, _ = tools_name.partition(':')

    match tools_name:
        case 'default':
            wiki = WikiToolFactory()
            return [
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
            llm = _build_llm_tool()
            return [
                LlmDialogTool(llm),
            ]
        case 'imgtool':
            return [
                ImageDumpTool(),
            ]
        case _:
            return None


def _build_tools_item(tools_item: str) -> list[ToolBase]:
    match tools_item:
        case 'web':
            return [
                WebSearchTool(),
                WebBrowseTool(),
            ]
        case 'wiki':
            wiki = WikiToolFactory()
            return [
                wiki.wiki_content(),
                wiki.wiki_summary(),
                wiki.wiki_section(),
                wiki.wiki_search(),
            ]
        case 'sh':
            return [
                ShellExecTool(),
                ShellCalcTool(),
            ]
        case 'llm':
            llm = _build_llm_tool()
            return [
                LlmDialogTool(llm),
            ]
        case 'img':
            return [
                ImageDumpTool(),
            ]
        case 'noop':
            return [
                DoNothingTool(),
            ]
        case _:
            raise ValueError


def _build_tools_list(tools_list: list[str] | None = None, env_ns: str = "") -> list[ToolBase]:
    env_ns = f"CHATIO_{env_ns}" if env_ns else "CHATIO"
    if tools_list is None:
        env_name = f"{env_ns}_TOOLS_LIST"
        tools_list_str = os.environ.get(env_name)
        if tools_list_str is None:
            tools_list_str = ""
        tools_list = tools_list_str.split(',')

    tools = []
    for tools_item in tools_list:
        if not tools_item:
            continue
        tools.extend(_build_tools_item(tools_item))

    return tools


def _build_tools_mode(tools_name: str | None = None, env_ns: str = "") -> tuple[str, str]:
    env_ns = f"CHATIO_{env_ns}" if env_ns else "CHATIO"
    if tools_name is None:
        env_name = f"{env_ns}_TOOLS_NAME"
        tools_name = os.environ.get(env_name)
        if not tools_name:
            tools_name = 'empty'

    _, _, tool_choice = tools_name.partition(':')
    tool_choice_mode, _, tool_choice_name = tool_choice.partition(':')

    return tool_choice_mode, tool_choice_name


def build_tools(
    tools_name: str | None = None,
    tools_list: list[str] | None = None,
    env_ns: str = "",
) -> ChatTools:
    tools = _build_tools_name(tools_name, env_ns)
    if tools is None:
        tools = _build_tools_list(tools_list, env_ns)

    tool_choice_mode, tool_choice_name = _build_tools_mode(tools_name, env_ns)

    return ChatTools(tools, tool_choice_mode, tool_choice_name)


def _build_llm_tool() -> Chat:
    env_ns = "NESTED"
    return Chat(
        model=build_model(env_ns=env_ns),
        tools=build_tools(env_ns=env_ns),
    )
