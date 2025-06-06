#!/usr/bin/env python

import sys
import dotenv
import logging

from chatio.api._common import ToolConfig

from chatio.api import build_chat
from chatio.cli.stdio import run_info, run_user, run_chat
from chatio.cli.style import Style
from chatio.misc import init_config

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.image import ImageDumpTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool, WebBrowseTool

# from toolbelt.llm import LlmDialogTool


logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('chatio.api').setLevel(logging.INFO)


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])

wiki = WikiToolFactory()

tools = {
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
}

# tools = {
#     "llm_message": LlmDialogTool(),
# }

# tools = {}

chat = build_chat(prompt, tools=ToolConfig(tools), config=init_config())


if __name__ == '__main__':
    run_info(chat, Style("::: ", color=Style.BRIGHT_GREEN))

    while True:
        print()
        content = run_user(Style(">>> ", color=Style.BRIGHT_GREEN))
        if content is None:
            break
        elif not content:
            continue

        chat.commit_chunk(content)

        print()
        run_chat(chat(),
                 model_style=Style("<<< ", color=Style.BRIGHT_CYAN),
                 event_style=Style("::: ", color=Style.RESET),
                 tools_style=Style("<<< ", color=Style.BRIGHT_MAGENTA))

    print()
