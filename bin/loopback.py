#!/usr/bin/env python

import sys
import pathlib

from chatio.cli.stdio import run_info, run_chat, run_text
from chatio.cli.style import Theme, Color

from chatio.misc import build_chat


def text_from(filepath: pathlib.Path) -> str | None:
    try:
        with filepath.open() as f:
            return f.read()
    except OSError as e:
        print(e, file=sys.stderr)
        return None


def main() -> None:

    themes = [
        Theme(direction=Theme.INPUT, color=Color.BRIGHT_GREEN),
        Theme(direction=Theme.OUTPUT, color=Color.BRIGHT_CYAN),
    ]

    script = pathlib.Path(sys.argv[1]) if sys.argv[1:] else pathlib.Path()

    request_prompt = text_from(script.joinpath('request.prompt'))
    if request_prompt:
        for prompt_line in request_prompt.splitlines():
            run_text("### " + prompt_line, themes[False].chunk_pri)
        print()

    response_prompt = text_from(script.joinpath('response.prompt'))
    if response_prompt:
        for prompt_line in response_prompt.splitlines():
            run_text("### " + prompt_line, themes[True].chunk_pri)
        print()

    with (
        build_chat(request_prompt, ["."]) as chat_request,
        build_chat(response_prompt) as chat_response,
    ):
        chats = [chat_request, chat_response]

        index = False

        messages_list = text_from(script.joinpath('messages.list'))
        if messages_list is not None:
            for content_raw in messages_list.splitlines():
                content = content_raw.strip()
                if not content:
                    continue

                chats[index].state.append_output_message(content)
                chats[not index].state.append_input_message(content)

                run_text(content, themes[index].chunk_pri)
                print()

                index = not index

        run_info(chats[index], themes[index])
        print()

        run_info(chats[not index], themes[not index])
        print()

        try:
            while True:
                content = run_chat(chats[index].stream_content(), themes[index])
                chats[not index].state.append_input_message(content)
                print()

                index = not index
        except KeyboardInterrupt:
            print()


if __name__ == '__main__':
    main()
