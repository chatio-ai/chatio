
import sys

from ._cli.build import build_chat

from ._cli.print import run_info
from ._cli import entry_point


@entry_point
async def main(*args: str) -> None:

    prompt = " ".join(args)
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit

    async with await build_chat(prompt, [content]) as chat:

        run_info(chat, file=sys.stderr)

        print(await chat.count_tokens())
