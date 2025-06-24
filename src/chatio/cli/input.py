
import atexit
import pathlib
import readline


from contextlib import suppress


class ChatCompleter:
    def complete(self, _text: str, state: int) -> str | None:
        line = readline.get_line_buffer()
        if line != line.rstrip():
            return None
        parts = line.split()
        if not all(part.startswith("@") for part in parts):
            return None

        part = parts.pop()
        path = pathlib.Path(part[1:])
        if part.endswith("/"):
            path_dir, path_name = path, ""
        else:
            path_dir, path_name = path.parent, path.name

        path_glob = path_dir.glob(f"{path_name}*")

        matches = [str(p.name) + "/" if p.is_dir() else str(p.name) + " " for p in path_glob]

        if state < len(matches):
            return matches[state]

        # print()
        # print(f"<{state}:{_text}:{part}:{path}:{matches}>")

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
        readline.set_completer(ChatCompleter())
        readline.parse_and_bind('tab: complete')

    def do_setup(self) -> None:
        if self._done:
            return

        self._do_setup_history()
        self._do_setup_complete()

        self._done = True


setup_readline = SetupReadLine()
