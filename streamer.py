#!/usr/bin/python

import sys
import dotenv

from chatutil import Chat, run_user, run_chat


dotenv.load_dotenv()

prompt = " ".join(sys.argv[1:])

chat = Chat(prompt)


if __name__ == '__main__':
    while True:
        content = run_user(">>> ")
        if content is None:
            break

        run_chat(chat, content, "<<< ")

    print()
