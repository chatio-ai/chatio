
from typing import override

from chatio.chat import ChatBase

from . import ToolBase


class LlmDialogTool(ToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Peform dialog to another LLM. Another LLM preserves history across session."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to pass to another LLM",
                },
            },
            "required": ["message"],
        }

    def __init__(self, agent: ChatBase):
        self._agent = agent

    def __call__(self, message=None):
        for event in self._agent(message):
            if event["type"] == 'model_chunk':
                yield event["text"]
