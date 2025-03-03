#!/usr/bin/env python

import sys
import dotenv
import logging
import pathlib

from chatio.api import build_chat
from chatio.misc import init_config
from chatio.cli import run_info, run_user, run_chat

logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('chatio.api').setLevel(logging.INFO)


dotenv.load_dotenv()

config = init_config()

prefix_chunks = [
    "\033[0;92m>>> ",
    "\033[0;96m<<< ",
]

prefix_events = [
    "\033[0;97m::: ",
    "\033[0;97m::: ",
]


def text_from(filepath):
    try:
        return filepath.open().read()
    except IOError as e:
        print(e, file=sys.stderr)
        return None


def file_from(filepath):
    try:
        return filepath.open()
    except IOError as e:
        print(e, file=sys.stderr)
        return None


if __name__ == '__main__':

    script = pathlib.Path(sys.argv[1]) if sys.argv[1:] else pathlib.Path()

    request_messages = []
    request_prompt = text_from(script.joinpath('request.prompt'))
    if request_prompt:
        print("###", prefix_chunks[False], request_prompt)

    response_messages = []
    response_prompt = text_from(script.joinpath('response.prompt'))
    if response_prompt:
        print("###", prefix_chunks[True], response_prompt)

    messages_list = file_from(script.joinpath('messages.list'))
    if messages_list:
        fetch_message = lambda: messages_list.readline()
    else:
        fetch_message = lambda: ""

    chats = [None, None]

    isbot = False

    content = None

    try:
        while True:

            this_messages = response_messages if isbot else request_messages
            this_prompt = response_prompt if isbot else request_prompt

            that_messages = request_messages if isbot else response_messages
            that_prompt = request_prompt if isbot else response_prompt

            if not chats[isbot]:
                content_raw = fetch_message()

                if content_raw:
                    if content:
                        if not request_messages:
                            request_messages.append(".")
                        request_messages.append(content)
                        response_messages.append(content)
                    content = content_raw.strip()

                    print(prefix_chunks[isbot], end="", flush=True)
                    print(content)

                if not content_raw:
                    chats[isbot] = build_chat(this_prompt, messages=this_messages[:], config=config)
                    run_info(chats[isbot])

            if chats[isbot]:
                if not content:
                    content = "."

                content = run_chat(chats[isbot], content,
                                   chunk_prefix=prefix_chunks[isbot],
                                   event_prefix=prefix_events[isbot])

                if not chats[not isbot]:
                    chats[not isbot] = build_chat(that_prompt, that_messages, config=config)
                    run_info(chats[not isbot])

            isbot = not isbot

            print()
    except KeyboardInterrupt:
        print()
