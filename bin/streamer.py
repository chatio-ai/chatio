#!/usr/bin/env python

import sys

from chatio.cli.stdio import run_info, run_user, run_chat
from chatio.cli.style import Style

from chatio.misc import setup_logging
from chatio.misc import default_tools
from chatio.misc import init_model
from chatio.misc import build_chat


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])

    chat = build_chat(prompt, model=init_model(), tools=default_tools())

    run_info(chat, Style("::: ", color=Style.BRIGHT_GREEN))

    while True:
        print()
        content = run_user(Style(">>> ", color=Style.BRIGHT_GREEN))
        if content is None:
            break
        if not content:
            continue

        chat.commit_input_message(content)

        print()
        run_chat(chat(),
                 model_style=Style("<<< ", color=Style.BRIGHT_CYAN),
                 event_style=Style("::: ", color=Style.RESET),
                 tools_style=Style("<<< ", color=Style.BRIGHT_MAGENTA))

    print()


if __name__ == '__main__':
    main()
