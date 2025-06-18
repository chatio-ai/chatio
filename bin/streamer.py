#!/usr/bin/env python

import sys


from chatio.cli.stdio import run_info, run_user_extra, run_chat
from chatio.cli.style import Style

from chatio.misc import setup_logging
from chatio.misc import init_model
from chatio.misc import init_state
from chatio.misc import init_tools
from chatio.misc import build_chat


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])

    chat = build_chat(model=init_model(), state=init_state(prompt), tools=init_tools())

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
            chat.attach_image_document(file=file)

        if content:
            chat.commit_input_message(content)

        chat.use_prediction_content(results)

        print()
        results = run_chat(chat(),
                           model_style=Style("<<< ", color=Style.BRIGHT_CYAN),
                           event_style=Style("::: ", color=Style.RESET),
                           tools_style=Style("<<< ", color=Style.BRIGHT_MAGENTA))

    print()


if __name__ == '__main__':
    main()
