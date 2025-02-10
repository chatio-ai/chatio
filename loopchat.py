#!/usr/bin/env python

import sys
import dotenv
import logging
import pathlib

from claudesy.api.claude import Chat as ClaudeChat
from claudesy.api.openai import Chat as OpenaiChat
from claudesy.ui import run_user, _run_chat, run_stat

logging.basicConfig(filename='chunkapi.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.getLogger('httpx').setLevel(logging.WARN)


dotenv.load_dotenv()

#Chat = ClaudeChat
#model = 'claude-3-5-haiku-latest'

Chat = OpenaiChat
model = 'gpt-4o-mini'

label = [
    ">>> ",
    "<<< ",
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
        print("###", label[False], request_prompt)

    response_messages = []
    response_prompt = text_from(script.joinpath('response.prompt'))
    if response_prompt:
        print("###", label[True], response_prompt)

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

                    print(label[isbot], end="", flush=True)
                    print(content)

                if not content_raw:
                    chats[isbot] = Chat(this_prompt, messages=this_messages[:], model=model)

            if chats[isbot]:
                if not content:
                    content = "."

                #print(chats[isbot], chats[isbot]._system, chats[isbot]._messages, content)
                events, content = _run_chat(chats[isbot], content, prefix=label[isbot])

                run_stat(events, "::: " + label[isbot], file=sys.stderr)

                if not chats[not isbot]:
                    chats[not isbot] = Chat(that_prompt, that_messages, model=model)

            isbot = not isbot

            print()
    except KeyboardInterrupt:
        print()
