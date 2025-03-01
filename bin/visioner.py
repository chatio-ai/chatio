#!/usr/bin/env python

import sys

import dotenv

from chatio.api import build_chat
from chatio.ui import run_chat, run_stat
from chatio.misc import init_config


from toolbelt.image import ImageDumpTool



dotenv.load_dotenv()

chat = build_chat(
    tool_choice='name',
    tool_choice_name='run_imgdump',
    tools={"run_imgdump": ImageDumpTool()},
    config=init_config(),
)


if __name__ == '__main__':

    content = []

    for filename in sys.argv[1:]:
        content.extend(chat.do_image(filename))

    if not content:
        raise SystemExit()

    events = run_chat(chat, content)

    run_stat(events)

    print()
