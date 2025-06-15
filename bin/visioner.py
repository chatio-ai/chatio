#!/usr/bin/env python

import sys

from chatio.cli.stdio import run_info, run_chat

from chatio.misc import setup_logging
from chatio.misc import default_tools
from chatio.misc import init_config
from chatio.misc import build_chat


setup_logging()


def main():
    chat = build_chat(config=init_config(), tools=default_tools(tools_name='imgtool'))

    filenames = sys.argv[1:]
    if not filenames:
        raise SystemExit

    for filename in filenames:
        chat.commit_image(filename)

    run_info(chat, "::: ")

    print()

    chat.commit_input_message(sys.stdin.read())
    run_chat(chat(), "<<< ", "::: ")

    print()


if __name__ == '__main__':
    main()
