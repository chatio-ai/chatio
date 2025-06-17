#!/usr/bin/env python

import sys

from chatio.cli.stdio import run_info

from chatio.misc import setup_logging
from chatio.misc import init_model
from chatio.misc import init_state
from chatio.misc import init_tools
from chatio.misc import build_chat


setup_logging()


def main():
    prompt = " ".join(sys.argv[1:])
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit

    chat = build_chat(state=init_state(prompt, [content]), model=init_model(), tools=init_tools())

    run_info(chat, file=sys.stderr)

    print(chat.count_tokens())


if __name__ == '__main__':
    main()
