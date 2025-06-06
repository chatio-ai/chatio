
from collections.abc import Mapping

from contextlib import suppress

from subprocess import Popen, PIPE, STDOUT

from . import ToolBase


class ShellToolBase(ToolBase):

    def _iterate(self, command=None, iterate=None):
        yield f"""```
$ {command}
"""

        with suppress(KeyboardInterrupt):
            yield from iterate

        yield f"""```
"""

    def __call__(self, command=None):

        process = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, text=True)

        yield from self._iterate(command, process.stdout)

        process.stdout.close()
        exit_code = process.wait()
        yield {'command': command, 'exit_code': exit_code}


class ShellCalcTool(ShellToolBase):

    __desc__: str = "Run bc command using system shell to evaluate the expression. Returns output of the command."

    __schema__: Mapping = {
        "type": "object",
        "properties": {
            "expr": {
                "type": "string",
                "description": "The expression to evaluate",
            },
        },
        "required": ["expr"],
    }

    def __init__(self):
        pass

    def __call__(self, expr):
        return super().__call__(f"echo '{expr}' | bc")


class ShellExecTool(ShellToolBase):

    __desc__: str = "Run custom user command using system shell. Returns output collected from stdout and stderr."

    __schema__: Mapping = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to run using system shell",
            },
        },
        "required": ["command"],
    }
