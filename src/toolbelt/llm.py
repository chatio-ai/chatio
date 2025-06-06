
from collections.abc import Mapping

from chatio.api import build_chat
from chatio.misc import init_config

from . import ToolBase


class LlmDialogTool(ToolBase):

    __desc__: str = "Peform request to another LLM. Another LLM preserves history across session."

    __schema__: Mapping = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to send to another LLM",
            },
        },
        "required": ["message"],
    }

    _agent = None

    def __call__(self, message=None):
        if not self._agent:
            self._agent = build_chat(config=init_config())

        for event in self._agent(message):
            if event["type"] == 'model_chunk':
                yield event["text"]
