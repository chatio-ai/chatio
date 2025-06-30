#!/usr/bin/env python

import sys


from chatio.cli.stdio import run_info, run_user_extra, run_chat
from chatio.cli.style import Style

from chatio.misc import setup_logging
from chatio.misc import build_chat


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])

    chat = build_chat(prompt)

    run_info(chat, Style("::: ", color=Style.BRIGHT_GREEN))

    results = None
    while True:
        print()
        content, files = run_user_extra(Style(">>> ", color=Style.BRIGHT_GREEN))
        if content is None:
            break
        if not files and not content:
            continue

        for file in files:
            chat.state.attach_document_auto(file=file)

        if content:
            chat.state.append_input_message(content)

        chat.state.update_prediction_state(results)

        print()
        results = run_chat(chat(),
                           model_style=Style("<<< ", color=Style.BRIGHT_CYAN),
                           event_style=Style("::: ", color=Style.RESET),
                           tools_style=Style("<<< ", color=Style.BRIGHT_MAGENTA))

    print()


if __name__ == '__main__':
    main()
