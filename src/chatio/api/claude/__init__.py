
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

    @property
    @override
    def format(self) -> ClaudeFormat:
        return ClaudeFormat(ClaudeConfigFormat(**self._config_format))

    @property
    @override
    def client(self) -> ClaudeClient:
        return ClaudeClient(ClaudeConfigClient(**self._config_client))


API = ClaudeFacadeDeps
