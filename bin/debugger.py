#!/usr/bin/env python

import sys

import dotenv

from chatio.api import build_chat
from chatio.cli import run_info, run_chat
from chatio.misc import init_config


def makechat():
    prompt = "Отвечай на русском"
    #prompt = "duplicate user message as is"
    #prompt = """
#You are 'determenistic parrot' system.
#Each user's message should be repeated back to them. Reproduce user message as verbatim as possible.
#Do not remove anything and do not add anything!
#"""

    messages = []

    #messages.append("How do you do? duplicate my message as is")
    #messages.append("How do you do? duplicate my message as is")

    #messages.append("<data>data</data>\n\nWhat is my data? duplicate my message as is")
    #messages.append("<data>data</data>\n\nWhat is my data? duplicate my message as is")

    #messages.append("[content description]\n\nWhat is my content about? duplicate my message as is")
    #messages.append("[content description]\n\nWhat is my content about? duplicate my message as is")

    #for _ in range(5):
    #    messages.append("[abra cadabra] something strange and not sdf;sljkdfs;ldk sdf <content>sdflskdgjlskdjgsldkgj</content> duplicate my message as is")
    #    messages.append("[abra cadabra] something strange and not sdf;sljkdfs;ldk sdf <content>sdflskdgjlskdjgsldkgj</content> duplicate my message as is")

    #for _ in range(5):
    #    messages.append("any random text and markup <data>here is the data</data>\n\nduplicate my message as is")
    #    messages.append("any random text and markup <data>here is the data</data>\n\nduplicate my message as is")

    for _ in range(5):
        messages.append("any random text and markup <data>here is the data</data>")
        messages.append("any random text and markup <data>here is the data</data>")

    for _ in range(5):
        messages.append("content.jpeg [Image depicting holy grail of Roman Empire]")
        messages.append("content.jpeg [Image depicting holy grail of Roman Empire]")

    return build_chat(prompt, messages, config=init_config())


dotenv.load_dotenv()

chat = makechat()


if __name__ == '__main__':

    run_info(chat)

    filenames = sys.argv[1:]
    for filename in filenames:
        chat.commit_image(filename)

    #chat.commit_chunk("duplicate my message as is")

    run_info(chat)

    print()

    if filenames:
        run_chat(chat, "<<< ")

    #chat.commit_chunk("what is the exact text on first image? duplicate my message as is")
    chat.commit_chunk("what is the exact text on first image?")

    run_chat(chat, "<<< ")

    print()
