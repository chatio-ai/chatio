
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import ClaudeFormatConfig
from .config import ClaudeClientConfig
from .params import ClaudeParams
from .format import ClaudeFormat
from .client import ClaudeClient


class ClaudeFacadeDeps(ApiFacadeDeps[
    ClaudeParams,
]):

    @property
    @override
    def format(self) -> ClaudeFormat:
        return ClaudeFormat(ClaudeFormatConfig(**self._config_format))

    @property
    @override
    def client(self) -> ClaudeClient:
        return ClaudeClient(ClaudeClientConfig(**self._config_client))


API = ClaudeFacadeDeps
