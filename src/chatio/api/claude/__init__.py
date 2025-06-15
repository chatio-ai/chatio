
from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam


from chatio.core.config import ChatConfig
from chatio.core.config import ChatApi


from .params import ClaudeParams
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeApi(ChatApi[
    TextBlockParam,
    MessageParam,
    TextBlockParam,
    ImageBlockParam,
    ToolParam,
    list[ToolParam],
]):

    def __init__(self, config: ChatConfig) -> None:
        super().__init__()

        self._config = config

        params = ClaudeParams(**config.config.options if config.config.options else {})

        self._format = ClaudeFormat(params)
        self._client = ClaudeClient(config.config, params)

    @property
    @override
    def config(self) -> ChatConfig:
        return self._config

    @property
    @override
    def format(self) -> ClaudeFormat:
        return self._format

    @property
    @override
    def client(self) -> ClaudeClient:
        return self._client
