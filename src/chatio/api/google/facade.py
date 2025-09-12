
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import GoogleConfigFormat
from .config import GoogleConfigClient
from .params import GoogleParams
from .format import GoogleFormat
from .client import GoogleClient


class GoogleFacadeDeps(ApiFacadeDeps[
    GoogleConfigFormat,
    GoogleParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:
        self._config = config

    @property
    @override
    def format(self) -> GoogleFormat:
        _config_format = GoogleConfigFormat(**self._config.get('format', {}))
        return GoogleFormat(_config_format)

    @property
    @override
    def client(self) -> GoogleClient:
        _config_client = GoogleConfigClient(**self._config.get('client', {}))
        return GoogleClient(_config_client)
