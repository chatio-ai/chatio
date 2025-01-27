#!/usr/bin/env python

import sys
import dotenv
import logging

from claudesy.api import Chat
from claudesy.ui import run_user, run_chat, run_stat

from toolbelt.shell import ShellCalcTool, ShellExecTool

from toolbelt.wiki import WikiToolFactory


logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])

wiki = WikiToolFactory()


chat = Chat(prompt, tools={
    "run_command": ShellExecTool(),
    "run_bc_calc": ShellCalcTool(),
    "wiki_content": wiki.wiki_content(),
    "wiki_summary": wiki.wiki_summary(),
    "wiki_section": wiki.wiki_section(),
    "wiki_search": wiki.wiki_search(),
})


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
