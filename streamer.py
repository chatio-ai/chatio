#!/usr/bin/python

import sys
import dotenv

from anthropic import Anthropic

dotenv.load_dotenv()

client = Anthropic()

if __name__ == '__main__':
    prompt = " ".join(sys.argv[1:])
    history = []

    while True:
        try:
            content = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            break

        history.append({"role": "user", "content": content})

        events = client.messages.stream(
                model='claude-3-5-sonnet-latest',
                system=prompt,
                max_tokens=4096,
                messages=history)

        with events as stream:
            print("<<< ", end="", flush=True)
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
            print()

            history.append({"role": "assistant", "content": stream.get_final_text()})

    print()
