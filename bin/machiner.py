#!/usr/bin/env python

import sys

from chatio.cli.stdio import run_text, run_user, run_chat

from chatio.misc import setup_logging
from chatio.misc import build_chat


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])

    chat = build_chat(prompt)

    while True:
        content_raw = run_user()
        if content_raw is None:
            break
        if not content_raw:
            continue

        content = content_raw.replace('\\n', '\n').replace('\\\\', '\\')

        run_text(content, ">>> ", file=sys.stderr)

        content = run_chat(chat(), content, "<<< ", file=sys.stderr)

        content_raw = content.replace('\\', '\\\\').replace('\n', '\\n')

        print(content_raw, end="", flush=True)

        print(file=sys.stderr)

    print()


if __name__ == '__main__':
    main()
