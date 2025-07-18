
import asyncio

from asyncio.subprocess import PIPE
from asyncio.subprocess import STDOUT

from collections.abc import AsyncIterator

from typing import override


from chatio.core.schema import ToolSchemaDict
from chatio.core.invoke import ToolBase


# pylint: disable=too-few-public-methods
class ShellToolBase(ToolBase):

    async def _iterate(self, command: str, iterate: AsyncIterator[bytes]) -> AsyncIterator[str]:
        yield f"""\
```
$ {command}
"""
        async for chunk in iterate:
            yield chunk.decode('utf-8')
        yield """\
```
"""

    async def _command(self, command: str) -> AsyncIterator[str | dict]:

        process = await asyncio.create_subprocess_shell(
                command, start_new_session=True, stdout=PIPE, stderr=STDOUT)

        try:
            if process.stdout is None:
                raise RuntimeError

            async for chunk in self._iterate(command, process.stdout):
                yield chunk
        finally:
            process.terminate()
            exit_code = await process.wait()
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
    def __call__(self, expr: str) -> AsyncIterator[str | dict]:
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
    def __call__(self, command: str) -> AsyncIterator[str | dict]:
        return self._command(command)
