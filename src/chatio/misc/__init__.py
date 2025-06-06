
import os

from chatio.api._common import ChatConfig
from chatio.api._common import ToolConfig

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.image import ImageDumpTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool, WebBrowseTool

# from toolbelt.llm import LlmDialogTool


def init_config():
    return ChatConfig(os.environ.get("CHATIO_PROVIDER_JSON", "./provider.json"))


def default_tools():
    wiki = WikiToolFactory()

    return ToolConfig({
        "run_command": ShellExecTool(),
        "run_bc_calc": ShellCalcTool(),
        "run_imgdump": ImageDumpTool(),
        "wiki_content": wiki.wiki_content(),
        "wiki_summary": wiki.wiki_summary(),
        "wiki_section": wiki.wiki_section(),
        "wiki_search": wiki.wiki_search(),
        "web_search": WebSearchTool(),
        "web_browse": WebBrowseTool(),
        "run_nothing": DummyTool(),
    })

    # tools = {
    #     "llm_message": LlmDialogTool(),
    # }

    # tools = {}
