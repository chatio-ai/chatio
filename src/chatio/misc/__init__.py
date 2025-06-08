
import os
import json
import logging

from pathlib import Path

from chatio.api._common import ApiConfig
from chatio.api._common import ChatConfig
from chatio.api._common import ToolConfig

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.image import ImageDumpTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool, WebBrowseTool

# from toolbelt.llm import LlmDialogTool


def setup_logging() -> None:
    logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')
    logging.getLogger('chatio.api').setLevel(logging.INFO)


def init_config(env_name: str | None = None) -> ChatConfig:
    if env_name is None:
        env_name = 'CHATIO_MODEL_NAME'

    model_name = os.environ.get(env_name)
    if not model_name or '/' not in model_name:
        err_msg = f"Configure {env_name}!"
        raise RuntimeError(err_msg)

    vendor_name, _, model_name = model_name.partition('/')
    vendor_conf = Path("./vendors").joinpath(vendor_name + ".json")

    with vendor_conf.open() as vendorfp:
        vendor_json = json.load(vendorfp)

    vendor_json = {k: v for k, v in vendor_json.items() if not k.startswith('_')}

    return ChatConfig(vendor_name, model_name, ApiConfig(**vendor_json))


def default_tools(env_name: str | None = None) -> ToolConfig:
    if env_name is None:
        env_name = 'CHATIO_TOOLS_CASE'

    tools_case = os.environ.get(env_name)
    if not tools_case:
        tools_case = 'empty'

    match tools_case:
        # case 'llmtool':
        #    return ToolConfig({
        #        "llm_message": LlmDialogTool(),
        #    })
        case 'default':
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
        case _:
            return ToolConfig()
