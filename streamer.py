#!/usr/bin/env python

import sys
import dotenv

from chatutil.api import Chat
from chatutil.ui import run_user, run_chat

from toolbelt.shell import ShellCalcTool, ShellExecTool


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

        run_chat(chat, content, "<<< ")

    print()
