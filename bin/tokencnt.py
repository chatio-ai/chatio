#!/usr/bin/env python

import sys

from chatio.cli.stdio import run_info

from chatio.misc import build_chat


def main() -> None:

    prompt = " ".join(sys.argv[1:])
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit

    with build_chat(prompt, [content]) as chat:

        run_info(chat, file=sys.stderr)

        print(chat.count_tokens())


if __name__ == '__main__':
    main()
