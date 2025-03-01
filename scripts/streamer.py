#!/usr/bin/env python

import os
import sys
import dotenv
import logging

from claudesy.api import build as chat_build
from claudesy.api import ChatConfig
from claudesy.ui import run_user, run_chat, run_stat

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.image import ImageDumpTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool, WebBrowseTool


logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

provider_file = os.environ.get("CLAUDESY_PROVIDER_JSON", "./provider.json")

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

chat = chat_build(prompt, config=ChatConfig(provider_file))


if __name__ == '__main__':
    while True:
        content = run_user(">>> ")
        if content is None:
            break
        elif not content:
            continue

        events = run_chat(chat, content, "<<< ")

        run_stat(events, "::: ")

    print()
