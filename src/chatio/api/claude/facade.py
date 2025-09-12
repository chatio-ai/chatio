
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import ClaudeConfigFormat
from .config import ClaudeConfigClient
from .params import ClaudeParams
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeFacadeDeps(ApiFacadeDeps[
    ClaudeConfigFormat,
    ClaudeParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:
        self._config = config

    @property
    @override
    def format(self) -> ClaudeFormat:
        _config_format = ClaudeConfigFormat(**self._config.get('format', {}))
        return ClaudeFormat(_config_format)

    @property
    @override
    def client(self) -> ClaudeClient:
        _config_client = ClaudeConfigClient(**self._config.get('client', {}))
        return ClaudeClient(_config_client)
