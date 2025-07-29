
import sys

from ._cli.build import build_chat

from ._cli.input import run_user
from ._cli.print import run_text, run_chat
from ._cli import entry_point


@entry_point
async def main(*args: str) -> None:

    prompt = " ".join(args)

    async with await build_chat(prompt) as chat:

        while True:
            content_raw = await run_user()
            if content_raw is None:
                break
            if not content_raw:
                continue

            content = content_raw.replace('\\n', '\n').replace('\\\\', '\\')

            run_text(content, file=sys.stderr)

            chat.state.append_input_message(content)

            content = await run_chat(chat.stream_content(), file=sys.stderr)

            content_raw = content.replace('\\', '\\\\').replace('\n', '\\n')

            print(content_raw, end="", flush=True)

            print(file=sys.stderr)

        print()
