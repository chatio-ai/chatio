#!/usr/bin/env python

import sys
import dotenv
import logging
import pathlib

from claudesy.api.default import Chat
from claudesy.ui import run_user, _run_chat, run_stat

logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

model = 'claude-3-5-sonnet-latest'

label = [
    ">>> ",
    "<<< ",
]


if __name__ == '__main__':

    script = pathlib.Path(sys.argv[1]) if sys.argv[1:] else pathlib.Path()

    try:
        request_prompt = script.joinpath('request.prompt').open().read()
    except Exception as e:
        print(e, file=sys.stderr)
        request_prompt = None

    try:
        response_prompt = script.joinpath('response.prompt').open().read()
    except Exception as e:
        print(e, file=sys.stderr)
        response_prompt = None

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
        Chat(request_prompt, messages=["."] + messages, model=model),
        Chat(response_prompt, messages=messages, model=model),
    ]

    while True:
        events, content = _run_chat(chats[isbot], content, prefix=label[isbot])

        run_stat(events, "::: ", file=sys.stderr)

        isbot = not isbot

        print()

    print()
