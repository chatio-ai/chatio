#!/usr/bin/env python

import sys

from chatio.api._common import ToolConfig

from chatio.api import build_chat
from chatio.cli.stdio import run_info, run_chat
from chatio.misc import init_config

from toolbelt.image import ImageDumpTool


def main():
    chat = build_chat(
        tools=ToolConfig(
            tools={"run_imgdump": ImageDumpTool()},
            tool_choice='name',
            tool_choice_name='run_imgdump',
        ),
        config=init_config(),
    )

    filenames = sys.argv[1:]
    if not filenames:
        raise SystemExit

    for filename in filenames:
        chat.commit_image(filename)

    run_info(chat, "::: ")

    print()

    chat.commit_chunk(sys.stdin.read())
    run_chat(chat(), "<<< ", "::: ")

    print()


if __name__ == '__main__':
    main()
