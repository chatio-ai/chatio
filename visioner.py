#!/usr/bin/python

import sys

import dotenv

from chatutil import Chat, do_image, run_chat


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

    return Chat(prompt, messages)


dotenv.load_dotenv()

chat = makechat()


if __name__ == '__main__':

    content = []

    for filename in sys.argv[1:]:
        content.extend(do_image(filename))

    #content.append({"type": "text", "text": "duplicate my message as is"})

    run_chat(chat, content)

    #run_chat(chat, "what is the exact text on first image? duplicate my message as is")
    run_chat(chat, "what is the exact text on first image?")
