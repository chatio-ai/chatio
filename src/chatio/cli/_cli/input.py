
import sys
import atexit
import pathlib
import readline

from contextlib import suppress

from pathlib import Path

from typing import TextIO


from .style import Theme, Input
from .style import _wrap_input
from .style import _wrap_print


class ChatCompleter:
    def complete(self, text: str, state: int) -> str | None:
        begidx = readline.get_begidx()
        line = readline.get_line_buffer()[:begidx]

        if not begidx or line[begidx - 1] != "@":
            return None

        if not all(p.startswith("@") for p in line.split()):
            return None

        path = pathlib.Path(text)
        if text.endswith("/"):
            path_dir, path_name = path, ""
        else:
            path_dir, path_name = path.parent, path.name

        path_glob = path_dir.glob(f"{path_name}*")

        matches = [f"{p}/" if p.resolve().is_dir() else f"{p} " for p in path_glob]

        if state < len(matches):
            return matches[state]

        return None

    def __call__(self, text: str, state: int) -> str | None:
        return self.complete(text, state)


class SetupReadLine:
    _HISTORY_FILE = '.chatio_history'

    def __init__(self) -> None:
        self._done = False

    def __call__(self) -> None:
        self.do_setup()

    def _do_setup_history(self) -> None:
        with suppress(FileNotFoundError):
            readline.read_history_file(self._HISTORY_FILE)

        atexit.register(readline.write_history_file, self._HISTORY_FILE)

    def _do_setup_complete(self) -> None:
        readline.set_completer_delims("@ \n\r\t\f")
        readline.set_completer(ChatCompleter())
        readline.parse_and_bind('tab: complete')

    def do_setup(self) -> None:
        if self._done:
            return

        self._do_setup_history()
        self._do_setup_complete()

        self._done = True


setup_readline = SetupReadLine()


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
