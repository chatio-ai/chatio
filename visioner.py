#!/usr/bin/env python

import sys

import dotenv

from claudesy.api import Chat, do_image
from claudesy.ui import run_chat


from toolbelt.image import ImageDumpTool



dotenv.load_dotenv()

chat = Chat(
    tool_choice='name',
    tool_choice_name='run_imgdump',
    tools={"run_imgdump": ImageDumpTool()},
)


if __name__ == '__main__':

    content = []

    for filename in sys.argv[1:]:
        content.extend(do_image(filename))

    if not content:
        raise SystemExit()

    run_chat(chat, content)

    print()
