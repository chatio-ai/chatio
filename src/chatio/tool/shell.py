
from collections.abc import Iterator

from typing import override

from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

from chatio.core.schema import ToolSchemaDict
from chatio.core.invoke import ToolBase


# pylint: disable=too-few-public-methods
class ShellToolBase(ToolBase):

    def _iterate(self, command: str, iterate: Iterator[str]) -> Iterator[str]:
        yield f"""\
```
$ {command}
"""
        yield from iterate
        yield """\
```
"""

    def _command(self, command: str) -> Iterator[str | dict]:

        with Popen(    # noqa: S602
                command, shell=True, start_new_session=True,
                stdout=PIPE, stderr=STDOUT, text=True) as process:

            try:
                if process.stdout is None:
                    raise RuntimeError

                yield from self._iterate(command, process.stdout)
            finally:
                process.terminate()
                exit_code = process.wait()
                yield f"# exit code: {exit_code}"
                yield {'command': command, 'exit_code': exit_code}


class ShellCalcTool(ShellToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "shell_calc",
            "description":
                "Run bc command via shell to evaluate expression. Returns output of the command.",
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "The expression to evaluate",
                },
            },
            "required": ["expr"],
        }

    @override
    def __call__(self, expr: str) -> Iterator[str | dict]:
        return self._command(f"echo '{expr}' | bc")


class ShellExecTool(ShellToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "shell_exec",
            "description":
                "Run custom user command via shell. Returns merged output from stdout and stderr.",
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to run using system shell",
                },
            },
            "required": ["command"],
        }

    @override
    def __call__(self, command: str) -> Iterator[str | dict]:
        return self._command(command)
