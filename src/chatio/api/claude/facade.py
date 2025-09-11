
from typing import override

from chatio.core.facade import ApiFacadeBase


from .config import ClaudeConfigFormat
from .config import ClaudeConfigClient
from .params import ClaudeParams
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeFacade(ApiFacadeBase[
    ClaudeConfigFormat,
    ClaudeParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_format = ClaudeConfigFormat(**config.get('format', {}))
        _config_client = ClaudeConfigClient(**config.get('client', {}))

        self._formatter = ClaudeFormat(_config_format)
        self._client_do = ClaudeClient(_config_client)

    @property
    @override
    def _format(self) -> ClaudeFormat:
        return self._formatter

    @property
    @override
    def _client(self) -> ClaudeClient:
        return self._client_do
