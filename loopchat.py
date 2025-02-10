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

    chats = [None, None]

    isbot = False

    messages = []

    try:
        while True:
            print(label[isbot], end="", flush=True)

            content = None
            if not chats[isbot]:
                content_raw = sys.stdin.readline()
                content = content_raw.strip()

                if content_raw:
                    if content:
                        messages.append(content)
                    content = content_raw.strip()
                    print(content)

                if not content_raw:
                    #messages = messages if isbot else ["."] + messages
                    prompt = response_prompt if isbot else request_prompt
                    chats[isbot] = Chat(prompt, messages=messages, model=model)

            if chats[isbot]:
                if not content:
                    content = "."
                events, content = _run_chat(chats[isbot], content, None)

                run_stat(events, "::: ", file=sys.stderr)

                if not chats[not isbot]:
                    messages = messages if isbot else messages + [content]
                    prompt = request_prompt if isbot else response_prompt
                    chats[not isbot] = Chat(prompt, messages, model=model)
                    print(chats[not isbot], chats[not isbot]._system, chats[not isbot]._messages)

            isbot = not isbot

            print()
    except KeyboardInterrupt:
        print()
