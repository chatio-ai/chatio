
import sys

from collections.abc import Iterable

from contextlib import suppress

from pathlib import Path

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


def _run_chat_event(event: dict, style: Style, file=None):

    etype = event.pop('type')
    etext = ""

    match etype:

        case 'token_usage':
            etext = f"token_usage: {event}"

        case 'tools_usage':
            etext = f"tools_usage: {event['tool_name']}: {event['tool_args']}"

        case 'tools_event':
            etext = f"tools_event: {event['tool_name']}: {event['tool_data']}"

        case _:
            raise RuntimeError

    with style.wrap_print(file=file):
        print(etext, end="", flush=True, file=file)


def _run_chat_chunk(chunk: str, style: Style, file=None, *, hascr: bool = False):
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


def _run_chat(events: Iterable[dict], model_style=None, event_style=None, tools_style=None, file=None):
    _model_style: Style = _mk_style(model_style)
    _tools_style: Style = _mk_style(tools_style)
    _event_style: Style = _mk_style(event_style)

    defer = None
    for event in events:
        etype = event.get("type")
        label = event.get("label")

        style = _event_style
        match etype, label:
            case "model_chunk", None:
                style = _model_style
            case "model_chunk", _:
                style = _tools_style
            case "tools_chunk", _:
                style = _tools_style

        if defer != style and defer:
            _run_chat_chunk('\n', style, file=file, hascr=not defer)
            defer = None

        chunk = event.get("text") or ""
        match etype:
            case "model_chunk":
                hascr = _run_chat_chunk(chunk, style, hascr=not defer, file=file)
                defer = None if hascr else style
                yield chunk
            case "tools_chunk":
                hascr = _run_chat_chunk(chunk, style, hascr=not defer, file=file)
                defer = None if hascr else style
            case _:
                _run_chat_event(event, style, file=file)
                defer = None


def run_chat(events: Iterable[dict], model_style=None, event_style=None, tools_style=None, file=None):
    return "".join(_run_chat(events, model_style, event_style, tools_style, file))
