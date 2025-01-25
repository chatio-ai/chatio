#!/usr/bin/env python

import sys
import dotenv

from chatutil.api import Chat
from chatutil.ui import run_user, run_chat


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])


def run_command(command=None):
    from subprocess import run, PIPE, STDOUT
    return run(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout.decode()


tools = [{
    "name": "run_command",
    "description": "Run custom user command using system shell",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to run using system shell",
            },
        },
        "required": ["command"],
    },
    "func": run_command,
}]


chat = Chat(prompt, tools=tools)


if __name__ == '__main__':
    while True:
        content = run_user(">>> ")
        if content is None:
            break

        run_chat(chat, content, "<<< ")

    print()
