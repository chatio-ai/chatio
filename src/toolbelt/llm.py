
from typing import override

from chatio.chat import Chat

from chatio.core.events import ModelTextChunk

from . import ToolBase


class LlmDialogTool(ToolBase):

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "name": "llm_dialog",
            "description": "Peform dialog to another LLM. Another LLM preserves history across session.",
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to pass to another LLM",
                },
            },
            "required": ["message"],
        }

    def __init__(self, agent: Chat):
        self._agent = agent

    def __call__(self, message=None):
        for event in self._agent(message):
            match event:
                case ModelTextChunk(text, _):
                    yield text
