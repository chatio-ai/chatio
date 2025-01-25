
import base64
import mimetypes

from anthropic import Anthropic

class Chat:
    def __init__(self, system=None, messages=None):
        self._client = Anthropic()
        self._stream = None

        self._system = system

        if messages is None:
            messages = []

        self._messages = []
        for index, message in enumerate(messages):
            self._messages.append(
                    self._user_message(message)
                    if not index % 2 else
                    self._ai_message(message))

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
