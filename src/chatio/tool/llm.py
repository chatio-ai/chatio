
from collections.abc import AsyncIterator

from typing import override

from chatio.chat import Chat

from chatio.core.events import ModelTextChunk

from chatio.core.schema import ToolSchemaDict
from chatio.core.invoke import ToolBase


class LlmDialogTool(ToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "llm_dialog",
            "description":
                "Peform dialog to another LLM. Another LLM preserves history across session.",
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to pass to another LLM",
                },
            },
            "required": ["message"],
        }

    def __init__(self, agent: Chat) -> None:
        self._agent = agent

    @override
    # pylint: disable=invalid-overridden-method
    async def __call__(self, message: str) -> AsyncIterator[str]:
        self._agent.state.append_input_message(message)
        async for event in self._agent.stream_content():
            match event:
                case ModelTextChunk(text, _):
                    yield text
