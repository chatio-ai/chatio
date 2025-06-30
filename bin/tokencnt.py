#!/usr/bin/env python

import sys

from chatio.cli.stdio import run_info

from chatio.misc import setup_logging
from chatio.misc import build_chat


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit

    chat = build_chat(prompt, [content])

    run_info(chat, file=sys.stderr)

    print(chat.count_tokens())


if __name__ == '__main__':
    main()
