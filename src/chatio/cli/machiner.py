
import sys

from chatio.misc import build_chat

from ._cli.stdio import run_text, run_user, run_chat


def main() -> None:

    prompt = " ".join(sys.argv[1:])

    with build_chat(prompt) as chat:

        while True:
            content_raw = run_user()
            if content_raw is None:
                break
            if not content_raw:
                continue

            content = content_raw.replace('\\n', '\n').replace('\\\\', '\\')

            run_text(content, file=sys.stderr)

            chat.state.append_input_message(content)

            content = run_chat(chat.stream_content(), file=sys.stderr)

            content_raw = content.replace('\\', '\\\\').replace('\n', '\\n')

            print(content_raw, end="", flush=True)

            print(file=sys.stderr)

        print()
