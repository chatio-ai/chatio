#!/usr/bin/env python

import sys
import dotenv
import logging

from chatio.api import build_chat
from chatio.misc import init_config
from chatio.cli.stdio import run_text, run_user, run_chat

logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('chatio.api').setLevel(logging.INFO)


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

        run_text(content, ">>> ", file=sys.stderr)

        content = run_chat(chat(), content, "<<< ", file=sys.stderr)

        content_raw = content.replace('\\', '\\\\').replace('\n', '\\n')

        print(content_raw, end="", flush=True)

        print(file=sys.stderr)

    print()
