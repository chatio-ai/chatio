#!/usr/bin/env python

import sys
import dotenv
import logging

from chatio.api import build_chat
from chatio.cli import run_info, run_user, run_chat
from chatio.cli.style import Style
from chatio.misc import init_config

logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('chatio.api').setLevel(logging.INFO)


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])

chat = build_chat(prompt, config=init_config())


if __name__ == '__main__':
    run_info(chat, Style("::: ", color=Style.BRIGHT_GREEN))

    results = None
    while True:
        print()
        content = run_user(Style(">>> ", color=Style.BRIGHT_GREEN))
        if content is None:
            break
        elif not content:
            continue

        chat.commit_chunk(content)

        print()
        results = run_chat(chat(prediction=results),
                           model_style=Style("<<< ", color=Style.BRIGHT_CYAN),
                           event_style=Style("::: ", color=Style.RESET),
                           tools_style=Style("<<< ", color=Style.BRIGHT_MAGENTA))

    print()
