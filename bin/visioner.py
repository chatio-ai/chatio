#!/usr/bin/env python

import sys

import dotenv

from chatio.api import build_chat
from chatio.cli import run_info, run_chat
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
    filenames = sys.argv[1:]
    if not filenames:
        raise SystemExit()

    for filename in filenames:
        chat.commit_image(filename)

    run_info(chat, "::: ")

    print()

    chat.commit_chunk(sys.stdin.read())
    run_chat(chat(), "<<< ", "::: ")

    print()
