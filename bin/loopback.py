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

    request_prompt = text_from(script.joinpath('request.prompt'))
    if request_prompt:
        print(prefix_chunks[False] + "###", request_prompt)

    response_prompt = text_from(script.joinpath('response.prompt'))
    if response_prompt:
        print(prefix_chunks[True] + "###", response_prompt)

    chats = [
        build_chat(request_prompt, messages=["."], config=config),
        build_chat(response_prompt, messages=None, config=config),
    ]

    index = False

    messages_list = file_from(script.joinpath('messages.list'))
    if messages_list:
        for content_raw in messages_list:
            content = content_raw.strip()
            if not content:
                continue

            chats[index].commit_chunk(content, model=True)
            chats[not index].commit_chunk(content)

            print(prefix_chunks[index], end="", flush=True)
            print(content)
            print()

            index = not index

    run_info(chats[index], prefix=prefix_chunks[index] + "::: ")
    print()

    run_info(chats[not index], prefix=prefix_chunks[not index] + "::: ")
    print()

    try:
        while True:
            content = run_chat(chats[index],
                               chunk_prefix=prefix_chunks[index],
                               event_prefix=prefix_events[index])

            chats[not index].commit_chunk(content)
            print()

            index = not index
    except KeyboardInterrupt:
        print()
