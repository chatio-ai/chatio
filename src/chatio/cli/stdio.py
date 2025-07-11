
import sys

from collections.abc import Iterable

from contextlib import suppress

from pathlib import Path


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import ToolEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk
from chatio.core.events import ToolsTextChunk


from .style import Style, Empty
from .input import setup_readline


def _mk_style(style=None) -> Style:
    if style is None:
        return Empty

    if isinstance(style, str):
        return Style(prefix=style)

    return style


def run_text(text, style=None, file=None):
    with _mk_style(style).wrap_print(file=file):
        print(text, end="", flush=True, file=file)


def run_info(chat, style=None, file=None):
    info = chat.info()

    run_text(
        f"chatio: model: {info.vendor}/{info.model} "
        f"tools: {info.tools} system: {info.system} messages: {info.messages}",
        style=style, file=file)


def run_user(style=None, file=None) -> str | None:
    setup_readline()

    user_input = None
    if sys.stdin.isatty():
        with (
            _mk_style(style).wrap_input(end="", file=file) as prompt,
            suppress(EOFError, KeyboardInterrupt),
        ):
            user_input = input(prompt)
    else:
        with suppress(EOFError, KeyboardInterrupt):
            user_input = input()
            with _mk_style(style).wrap_print(end="", file=file):
                print(user_input, flush=True, file=file)

    return user_input


def run_user_extra(style=None, file=None) -> tuple[str | None, list[Path]]:
    user_input = run_user(style, file)
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


def _run_chat_event(event: ChatEvent, style: Style, file=None):

    match event:

        case StatEvent(label, delta, total):
            text = f"stat: {label}: {delta} of {total}"

        case CallEvent(_, name, args, _):
            text = f"call: {name}: {args}"

        case ToolEvent(_, name, data):
            text = f"tool: {name}: {data}"

        case _:
            raise RuntimeError

    with style.wrap_print(file=file):
        print(text, end="", flush=True, file=file)


def _run_text_chunk(chunk: str, style: Style, file=None, *, hascr: bool = False):
    for chunk_line in chunk.splitlines(keepends=True):
        result = ""
        if hascr:
            result += style.color + style.prefix

        hascr = chunk_line.endswith("\n")
        if hascr:
            result += chunk_line[:-1]
            result += style.suffix
            result += "\n"
        else:
            result += chunk_line

        print(result, end="", flush=True, file=file)

    return hascr


def _run_chat(events: Iterable[ChatEvent], model_style=None, event_style=None, tools_style=None, file=None):
    _model_style: Style = _mk_style(model_style)
    _tools_style: Style = _mk_style(tools_style)
    _event_style: Style = _mk_style(event_style)

    defer = None
    for event in events:
        style = _event_style
        match event:
            case ModelTextChunk(_, label) if label is None:
                style = _model_style
            case ModelTextChunk():
                style = _tools_style
            case ToolsTextChunk():
                style = _tools_style
            # case _:
            #     style = _event_style

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


def run_chat(events: Iterable[ChatEvent], model_style=None, event_style=None, tools_style=None, file=None):
    return "".join(_run_chat(events, model_style, event_style, tools_style, file))
