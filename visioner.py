#!/usr/bin/python

import sys
import base64
import mimetypes

import dotenv

from anthropic import Anthropic

class Chat:
    def __init__(self):
        self._client = Anthropic()
        #self._system = "duplicate user message as is"
        #self._system = "Отвечай на русском"
        self._system = "You are 'determenistic parrot' system. Each user's message should be repeated back to them. Reproduce user message as verbatim as possible." \
                "Do not remove anything and do not add anything!"
        self._stream = None

        self._messages = []

        #self._messages.append(self._user_message("How do you do? duplicate my message as is"))
        #self._messages.append(self._ai_message("How do you do? duplicate my message as is"))

        #self._messages.append(self._user_message("<data>data</data>\n\nWhat is my data? duplicate my message as is"))
        #self._messages.append(self._ai_message("<data>data</data>\n\nWhat is my data? duplicate my message as is"))

        #self._messages.append(self._user_message("[content description]\n\nWhat is my content about? duplicate my message as is"))
        #self._messages.append(self._ai_message("[content description]\n\nWhat is my content about? duplicate my message as is"))

        #for _ in range(5):
        #    self._messages.append(self._user_message("[abra cadabra] something strange and not sdf;sljkdfs;ldk sdf <content>sdflskdgjlskdjgsldkgj</content> duplicate my message as is"))
        #    self._messages.append(self._ai_message("[abra cadabra] something strange and not sdf;sljkdfs;ldk sdf <content>sdflskdgjlskdjgsldkgj</content> duplicate my message as is"))

        #for _ in range(5):
        #    self._messages.append(self._user_message("any random text and markup <data>here is the data</data>\n\nduplicate my message as is"))
        #    self._messages.append(self._ai_message("any random text and markup <data>here is the data</data>\n\nduplicate my message as is"))

        for _ in range(5):
            self._messages.append(self._user_message("any random text and markup <data>here is the data</data>"))
            self._messages.append(self._ai_message("any random text and markup <data>here is the data</data>"))

        for _ in range(5):
            self._messages.append(self._user_message("content.jpeg [Image depicting holy grail of Roman Empire]"))
            self._messages.append(self._ai_message("content.jpeg [Image depicting holy grail of Roman Empire]"))

    def _user_message(self, content):
        return {"role": "user", "content": content}

    def _ai_message(self, content):
        return {"role": "assistant", "content": content}

    def __call__(self, content):
        if self._stream is not None:
            with self._stream as stream:
                self._messages.append(self._ai_message(stream.get_final_text()))

        self._messages.append(self._user_message(content))

        self._stream = self._client.messages.stream(
            model='claude-3-5-sonnet-latest',
            max_tokens=4096,
            system=self._system,
            messages=self._messages)

        return self._stream


def run_chat(chat, content):
    with chat(content) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
        print()


def do_image(filename):
    content = []

    with open(filename, "rb") as file:
        data = file.read()
        data_as_base64 = base64.b64encode(data)
        data_as_string = data_as_base64.decode()
        mimetype, _ = mimetypes.guess_type(filename)

        content.append({
            "type": "text",
            "text": filename,
        })

        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mimetype,
                "data": data_as_string,
            }
        })

    return content


dotenv.load_dotenv()

chat = Chat()


if __name__ == '__main__':
    content = []

    for filename in sys.argv[1:]:
        content.extend(do_image(filename))

    #content.append({"type": "text", "text": "duplicate my message as is"})

    run_chat(chat, content)

    #run_chat(chat, "what is the exact text on first image? duplicate my message as is")
    run_chat(chat, "what is the exact text on first image?")
