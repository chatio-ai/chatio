
import re
import sys

from collections.abc import Iterable
from collections.abc import Iterator

from contextlib import suppress

from pathlib import Path

from typing import TextIO


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import ToolEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk
from chatio.core.events import ToolsTextChunk

from chatio.chat import Chat


from .style import Theme, Input, Model
from .style import Style, Empty
from .input import setup_readline


class StyleWrap:

    def __init__(
        self, style: Style, end: str | None = None,
        file: TextIO | None = None, *, prompt: bool = False,
    ) -> None:
        self.style = style
        self.file = file
        self.end = end
        self.prompt = prompt

    def __enter__(self) -> str:
        if self.prompt:
            return re.sub('\033\\[[0-9;]*m', '\001\\g<0>\002', self.style.prefix)

        print(self.style.prefix, end="", flush=True, file=self.file)
        return ""

    def __exit__(self, *exc: object) -> None:
        print(self.style.suffix, end=self.end, flush=True, file=self.file)


def _wrap_print(style: Style, end: str | None = None, file: TextIO | None = None) -> StyleWrap:
    return StyleWrap(style, end=end, file=file)


def _wrap_input(style: Style, end: str | None = None, file: TextIO | None = None) -> StyleWrap:
    return StyleWrap(style, end=end, file=file, prompt=True)


def run_text(text: str, style: Style | None = None, *, file: TextIO | None = None) -> None:
    if style is None:
        style = Empty
    with _wrap_print(style, file=file):
        print(text, end="", flush=True, file=file)


def run_info(chat: Chat, theme: Theme | None = None, *, file: TextIO | None = None) -> None:
    info = chat.info()

    if theme is None:
        theme = Model

    run_text(
        f"chatio: model: {info.vendor}/{info.model} "
        f"tools: {info.tools} system: {info.system} messages: {info.messages}",
        style=theme.event_pri, file=file)


def run_user(theme: Theme | None = None, *, file: TextIO | None = None) -> str | None:
    setup_readline()

    if theme is None:
        theme = Input

    user_input = None
    if sys.stdin.isatty():
        with (
            _wrap_input(theme.chunk_pri, end="", file=file) as prompt,
            suppress(EOFError, KeyboardInterrupt),
        ):
            user_input = input(prompt)
    else:
        with suppress(EOFError, KeyboardInterrupt):
            user_input = input()
            with _wrap_print(theme.chunk_pri, end="", file=file):
                print(user_input, flush=True, file=file)

    return user_input


def run_user_extra(theme: Theme | None = None, *,
                   file: TextIO | None = None) -> tuple[str | None, list[Path]]:

    user_input = run_user(theme, file=file)
    if user_input is None:
        return None, []

    paths = []
    ready = True
    while ready:
        ready = False
        splits = user_input.split(maxsplit=1)

        part, rest = "", ""
        match len(splits):
            case 2:
                part, rest = splits
            case 1:
                part = splits.pop()
            case _:
                pass

        if part.startswith("@"):
            paths.append(Path(part.removeprefix("@")))
            user_input = rest
            ready = True

    return user_input, paths


def _run_chat_event(event: ChatEvent, style: Style, *, file: TextIO | None = None) -> None:

    match event:

        case StatEvent(label, delta, total):
            text = f"stat: {label}: {delta} of {total}"

        case CallEvent(_, name, args, _):
            text = f"call: {name}: {args}"

        case ToolEvent(_, name, data):
            text = f"tool: {name}: {data}"

        case _:
            raise RuntimeError

    with _wrap_print(style, file=file):
        print(text, end="", flush=True, file=file)


def _run_text_chunk(chunk: str, style: Style, *,
                    hascr: bool = False, file: TextIO | None = None) -> bool:

    for chunk_line in chunk.splitlines(keepends=True):
        result = ""
        if hascr:
            result += style.prefix

        hascr = chunk_line.endswith("\n")
        if hascr:
            result += chunk_line[:-1]
            result += style.suffix
            result += "\n"
        else:
            result += chunk_line

        print(result, end="", flush=True, file=file)

    return hascr


def _run_chat(events: Iterable[ChatEvent], theme: Theme | None = None, *,
              file: TextIO | None = None) -> Iterator[str]:

    if theme is None:
        theme = Model

    defer = None
    for event in events:
        style = theme.event_sec
        match event:
            case ModelTextChunk(_, label) if label is None:
                style = theme.chunk_pri
            case ModelTextChunk():
                style = theme.chunk_sec
            case ToolsTextChunk():
                style = theme.chunk_sec

        if defer != style and defer:
            _run_text_chunk('\n', style, file=file, hascr=not defer)
            defer = None

        match event:
            case ModelTextChunk(chunk, _):
                hascr = _run_text_chunk(chunk, style, hascr=not defer, file=file)
                defer = None if hascr else style
                yield chunk
            case ToolsTextChunk(chunk, _):
                hascr = _run_text_chunk(chunk, style, hascr=not defer, file=file)
                defer = None if hascr else style
            case _:
                _run_chat_event(event, style, file=file)
                defer = None


def run_chat(events: Iterable[ChatEvent], theme: Theme | None = None, *,
             file: TextIO | None = None) -> str:

    return "".join(_run_chat(events, theme, file=file))
