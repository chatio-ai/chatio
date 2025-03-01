#!/usr/bin/env python

import sys
import dotenv
import logging

from chatio.api import build_chat
from chatio.misc import init_config
from chatio.ui import run_user, run_chat, run_stat

logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])

chat = build_chat(prompt, config=init_config())


if __name__ == '__main__':
    while True:
        content_raw = run_user()
        if content_raw is None:
            break
        elif not content_raw:
            continue

        content = content_raw.replace('\\n', '\n').replace('\\\\', '\\')

        print(">>>", content, file=sys.stderr)
        print("", file=sys.stderr)
        print("<<<", "", end="", flush=True, file=sys.stderr)

        events = run_chat(chat, content, file=sys.stderr)

        print("", file=sys.stderr)
        print("", file=sys.stderr)

        run_stat(events, "::: ", file=sys.stderr)

        print("", file=sys.stderr)

    print()
