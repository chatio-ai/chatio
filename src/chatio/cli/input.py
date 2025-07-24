
import atexit
import pathlib
import readline


from contextlib import suppress


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
