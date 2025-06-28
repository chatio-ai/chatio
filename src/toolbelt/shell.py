
from collections.abc import Iterable

from typing import override

from contextlib import suppress

from subprocess import Popen, PIPE, STDOUT

from . import ToolBase


# pylint: disable=too-few-public-methods
class ShellToolBase(ToolBase):

    def _iterate(self, command: str, iterate: Iterable[str]):
        yield f"""```
$ {command}
"""

        with suppress(KeyboardInterrupt):
            yield from iterate

        yield f"""```
"""

    def _command(self, command: str):

        with Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, text=True) as process:
            if process.stdout is not None:
                yield from self._iterate(command, process.stdout)
                process.stdout.close()

            exit_code = process.wait()
            yield {'command': command, 'exit_code': exit_code}


class ShellCalcTool(ShellToolBase):

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "name": "shell_calc",
            "description": "Run bc command via shell to evaluate expression. Returns output of the command.",
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "The expression to evaluate",
                },
            },
            "required": ["expr"],
        }

    def __call__(self, expr: str):
        return self._command(f"echo '{expr}' | bc")


class ShellExecTool(ShellToolBase):

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "name": "shell_exec",
            "description": "Run custom user command via shell. Returns merged output from stdout and stderr.",
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to run using system shell",
                },
            },
            "required": ["command"],
        }

    def __call__(self, command: str):
        return self._command(command)
