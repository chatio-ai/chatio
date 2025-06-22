
from typing import override

from chatio.core.config import ApiConfig
from chatio.core.params import ApiParams
from chatio.core import ApiHelper

from chatio.api.claude.config import ClaudeConfig
from chatio.api.claude.params import ClaudeParams

from chatio.api.openai.config import OpenAIConfig
from chatio.api.openai.client import OpenAIClient


class CustomApi(ApiHelper[ApiParams]):

    def __init__(self, claude_config: ClaudeConfig, openai_config: OpenAIConfig) -> None:

        self._params = ClaudeParams(claude_config)
        self._client = OpenAIClient(openai_config)

    @property
    @override
    def config(self) -> ApiConfig:
        raise NotImplementedError

    @property
    @override
    def params(self) -> ClaudeParams:
        return self._params

    @property
    @override
    def client(self) -> OpenAIClient:
        return self._client
