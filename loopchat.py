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


def prompt_from(filepath):
    try:
        return filepath.open().read()
    except IOError as e:
        print(e, file=sys.stderr)
        return None


if __name__ == '__main__':

    script = pathlib.Path(sys.argv[1]) if sys.argv[1:] else pathlib.Path()

    request_prompt = prompt_from(script.joinpath('request.prompt'))
    if request_prompt:
        print("###", label[False], request_prompt)

    response_prompt = prompt_from(script.joinpath('response.prompt'))
    if response_prompt:
        print("###", label[True], response_prompt)

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

    try:
        while True:
            events, content = _run_chat(chats[isbot], content, prefix=label[isbot])

            run_stat(events, "::: ", file=sys.stderr)

            isbot = not isbot

            print()
    except KeyboardInterrupt:
        print()
