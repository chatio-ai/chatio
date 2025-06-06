#!/usr/bin/env python

import sys
import logging

from chatio.api import build_chat
from chatio.cli.stdio import run_info, run_user, run_chat
from chatio.cli.style import Style
from chatio.misc import init_config, default_tools


logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('chatio.api').setLevel(logging.INFO)


def main():
    prompt = " ".join(sys.argv[1:])

    chat = build_chat(prompt, tools=default_tools(), config=init_config())

    run_info(chat, Style("::: ", color=Style.BRIGHT_GREEN))

    while True:
        print()
        content = run_user(Style(">>> ", color=Style.BRIGHT_GREEN))
        if content is None:
            break
        if not content:
            continue

        chat.commit_chunk(content)

        print()
        run_chat(chat(),
                 model_style=Style("<<< ", color=Style.BRIGHT_CYAN),
                 event_style=Style("::: ", color=Style.RESET),
                 tools_style=Style("<<< ", color=Style.BRIGHT_MAGENTA))

    print()


if __name__ == '__main__':
    main()
