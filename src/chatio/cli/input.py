
import atexit
import readline

from contextlib import suppress


class SetupHistory:
    _HISTORY_FILE = '.chatio_history'

    def __init__(self):
        self._done = False

    def __call__(self):
        self.do_setup()

    def do_setup(self):
        if self._done:
            return

        with suppress(FileNotFoundError):
            readline.read_history_file(self._HISTORY_FILE)

        atexit.register(readline.write_history_file, self._HISTORY_FILE)

        self._done = True


setup_history = SetupHistory()
