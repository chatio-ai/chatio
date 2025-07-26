
import sys

from chatio.misc import build_chat

from ._cli.stdio import run_info


def main() -> None:

    prompt = " ".join(sys.argv[1:])
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit

    with build_chat(prompt, [content]) as chat:

        run_info(chat, file=sys.stderr)

        print(chat.count_tokens())
