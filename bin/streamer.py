#!/usr/bin/env python

import sys
import dotenv
import logging

from chatio.api import build_chat
from chatio.cli import run_info, run_user, run_chat
from chatio.misc import init_config

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.image import ImageDumpTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool, WebBrowseTool


logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


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

#tools = {}

chat = build_chat(prompt, tools=tools, config=init_config())


if __name__ == '__main__':
    run_info(chat)

    while True:
        print()
        content = run_user(">>> ")
        if content is None:
            break
        elif not content:
            continue

        print()
        run_chat(chat, content, "<<< ")

    print()
