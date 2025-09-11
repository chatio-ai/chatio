
from typing import override

from chatio.core.facade import ApiFacadeBase


from .config import GoogleConfigFormat
from .config import GoogleConfigClient
from .params import GoogleParams
from .format import GoogleFormat
from .client import GoogleClient


class GoogleFacade(ApiFacadeBase[
    GoogleConfigFormat,
    GoogleParams,
]):

    def __init__(self, config: dict[str, dict]) -> None:

        _config_client = GoogleConfigClient(**config.get('client', {}))
        _config_format = GoogleConfigFormat(**config.get('format', {}))

        self._formatter = GoogleFormat(_config_format)
        self._client_do = GoogleClient(_config_client)

    @property
    @override
    def _format(self) -> GoogleFormat:
        return self._formatter

    @property
    @override
    def _client(self) -> GoogleClient:
        return self._client_do
