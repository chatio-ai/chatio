
from typing import override

from anthropic.types import MessageParam

from anthropic.types import ToolParam
from anthropic.types import ToolChoiceParam
from anthropic.types import TextBlockParam
from anthropic.types import ImageBlockParam


from chatio.core.config import ApiHelper
from chatio.core.config import ModelConfig


from .config import ClaudeConfig
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeApi(ApiHelper[
    TextBlockParam,
    MessageParam,
    None,
    TextBlockParam,
    ImageBlockParam,
    ToolParam,
    list[ToolParam],
    ToolChoiceParam,
]):

    def __init__(self, model: ModelConfig, config: ClaudeConfig) -> None:
        self._model = model

        # params = ClaudeParams(**config.config.api if config.config.api else {})

        self._format = ClaudeFormat(config)
        self._client = ClaudeClient(config)

    @property
    @override
    def config(self) -> ModelConfig:
        return self._model

    @property
    @override
    def format(self) -> ClaudeFormat:
        return self._format

    @property
    @override
    def client(self) -> ClaudeClient:
        return self._client
