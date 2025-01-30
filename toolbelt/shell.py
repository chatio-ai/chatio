
from subprocess import run, PIPE, STDOUT

from . import ToolBase


class ShellToolBase(ToolBase):

    def __call__(self, command=None):
        yield run(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout.decode()


class ShellCalcTool(ShellToolBase):

    __desc__ = "Run bc command using system shell to evaluate the expression. Returns output of the command."

    __schema__ = {
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

    __desc__ = "Run custom user command using system shell. Returns output collected from stdout and stderr streams."

    __schema__ = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to run using system shell",
            },
        },
        "required": ["command"],
    }
