#!/usr/bin/env python

import sys
import dotenv
import logging

from claudesy.api.default import Chat
from claudesy.ui import run_user, _run_chat, run_stat

logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])

model = 'claude-3-5-sonnet-latest'

label = [
    ">>> ",
    "<<< ",
]


if __name__ == '__main__':

    isbot = False

    content = "."
    messages = []

    while True:
        print(label[isbot], end="", flush=True)

        content_raw = sys.stdin.readline()
        if not content_raw:
            break

        content = content_raw.strip()
        print(content)

        messages.append(content)

        isbot = not isbot

    chats = [
        Chat(prompt, messages=["."] + messages, model=model),
        Chat(prompt, messages=messages, model=model),
    ]

    while True:
        events, content = _run_chat(chats[isbot], content, prefix=label[isbot])

        run_stat(events, "::: ", file=sys.stderr)

        isbot = not isbot

    print()
