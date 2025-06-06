#!/usr/bin/env python

import sys

from chatio.api import build_chat
from chatio.cli.stdio import run_info
from chatio.misc import init_config, default_tools


def main():
    prompt = " ".join(sys.argv[1:])
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit

    chat = build_chat(prompt, messages=[content], tools=default_tools(), config=init_config())

    run_info(chat, file=sys.stderr)

    print(chat.count_tokens())


if __name__ == '__main__':
    main()
