#!/usr/bin/env python

import sys
import dotenv
import logging

from chatutil.api import Chat
from chatutil.ui import run_user, run_chat

from toolbelt.shell import ShellCalcTool, ShellExecTool


logging.basicConfig(filename='chatbot.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])


chat = Chat(prompt, tools={
    "run_command": ShellExecTool(),
    "run_bc_calc": ShellCalcTool(),
})


if __name__ == '__main__':
    while True:
        content = run_user(">>> ")
        if content is None:
            break
        elif not content:
            continue

        run_chat(chat, content, "<<< ")

    print()
