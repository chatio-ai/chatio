#!/usr/bin/env python

import sys

from chatio.api import build_chat
from chatio.cli.stdio import run_text, run_user, run_chat
from chatio.misc import init_config
from chatio.misc import setup_logging


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])

    chat = build_chat(prompt, config=init_config())

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
