
import os


from chatio.chat.tools import ChatTools

from toolbelt.shell import ShellCalcTool
from toolbelt.shell import ShellExecTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool
from toolbelt.web import WebBrowseTool

from toolbelt.image import ImageDumpTool

from toolbelt.llm import LlmDialogTool


def build_tools(tools_name: str | None = None, env_name: str | None = None) -> ChatTools:
    if tools_name is not None and env_name is not None:
        raise ValueError

    if tools_name is None:
        if env_name is None:
            env_name = 'CHATIO_TOOLS_NAME'

        tools_name = os.environ.get(env_name)
        if not tools_name:
            tools_name = 'empty'

    tools_name, _, tool_choice = tools_name.partition(':')
    tool_choice_mode, _, tool_choice_name = tool_choice.partition(':')

    tools: dict | None = None
    match tools_name:
        case 'default':
            wiki = WikiToolFactory()

            tools = {
                "run_command": ShellExecTool(),
                "run_bc_calc": ShellCalcTool(),
                "wiki_content": wiki.wiki_content(),
                "wiki_summary": wiki.wiki_summary(),
                "wiki_section": wiki.wiki_section(),
                "wiki_search": wiki.wiki_search(),
                "web_search": WebSearchTool(),
                "web_browse": WebBrowseTool(),
                "run_nothing": DummyTool(),
            }
        case 'llmtool':
            llm = build_llm_tool()

            tools = {
                "llm_message": LlmDialogTool(llm),
            }
        case 'imgtool':
            tools = {
                "run_imgdump": ImageDumpTool(),
            }

    return ChatTools(tools, tool_choice_mode=tool_choice_mode, tool_choice_name=tool_choice_name)


def build_llm_tool():
    raise NotImplementedError
