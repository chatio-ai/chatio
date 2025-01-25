#!/usr/bin/python

import sys

import dotenv

from anthropic import Anthropic


dotenv.load_dotenv()

client = Anthropic()


if __name__ == '__main__':
    content = sys.stdin.read()
    if not content.strip():
        print(0)
        raise SystemExit()

    usage = client.messages.count_tokens(
            model='claude-3-5-sonnet-latest',
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": content}
                ]},
            ])

    print(usage.input_tokens)
