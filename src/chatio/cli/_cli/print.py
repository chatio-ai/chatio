
from collections.abc import AsyncIterable
from collections.abc import AsyncIterator

from typing import TextIO


from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import ToolEvent
from chatio.core.events import StatEvent
from chatio.core.events import StopEvent
from chatio.core.events import ModelTextChunk
from chatio.core.events import ToolsTextChunk

from chatio.chat import ChatReply
from chatio.chat import Chat


from .style import Theme, Model
from .style import Style, Empty
from .style import _wrap_print


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


async def _run_chat(events: AsyncIterable[ChatEvent], theme: Theme | None = None, *,
                    file: TextIO | None = None) -> AsyncIterator[str]:

    if theme is None:
        theme = Model

    defer = None
    async for event in events:
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
            case StopEvent(_):
                pass
            case _:
                _run_chat_event(event, style, file=file)
                defer = None


async def run_chat(reply: ChatReply, theme: Theme | None = None, *,
                   file: TextIO | None = None) -> str:

    async with reply as events:
        return "".join([_ async for _ in _run_chat(events, theme, file=file)])
