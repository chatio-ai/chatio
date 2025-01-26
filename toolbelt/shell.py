
from subprocess import run, PIPE, STDOUT

from . import ToolBase


class ShellCalcTool(ToolBase):

    __desc__ = "Run bc command to evaluate the expression"

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
        return run(f"echo '{expr}' | bc", shell=True, stdout=PIPE, stderr=STDOUT).stdout.decode()


class ShellExecTool(ToolBase):

    __desc__ = "Run custom user command using system shell"

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

    def __call__(self, command=None):
        return run(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout.decode()

