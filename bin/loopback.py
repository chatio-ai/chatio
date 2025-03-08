#!/usr/bin/env python

import sys
import dotenv
import logging
import pathlib

from chatio.api import build_chat
from chatio.misc import init_config
from chatio.cli import run_info, run_user, run_chat, run_text
from chatio.cli import Style

logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('chatio.api').setLevel(logging.INFO)


dotenv.load_dotenv()

config = init_config()

model_styles = [
    Style(">>> ", color=Style.BRIGHT_GREEN),
    Style("<<< ", color=Style.BRIGHT_CYAN),
]

banner_styles = [
    Style("::: ", color=Style.BRIGHT_GREEN),
    Style("::: ", color=Style.BRIGHT_CYAN),
]

prompt_styles = [
    Style("### >>> ", color=Style.BRIGHT_GREEN),
    Style("### <<< ", color=Style.BRIGHT_CYAN),
]

event_styles = [
    Style("::: "),
    Style("::: "),
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
        run_text(request_prompt, prompt_styles[False])

    response_prompt = text_from(script.joinpath('response.prompt'))
    if response_prompt:
        run_text(response_prompt, prompt_styles[True])

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

            run_text(content, model_styles[index])
            print()

            index = not index

    run_info(chats[index], banner_styles[index])
    print()

    run_info(chats[not index], banner_styles[not index])
    print()

    try:
        while True:
            content = run_chat(chats[index](),
                               model_style=model_styles[index],
                               event_style=event_styles[index])

            chats[not index].commit_chunk(content)
            print()

            index = not index
    except KeyboardInterrupt:
        print()
