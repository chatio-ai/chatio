
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import GoogleFormatConfig
from .config import GoogleClientConfig
from .params import GoogleParams
from .format import GoogleFormat
from .client import GoogleClient


class GoogleFacadeDeps(ApiFacadeDeps[
    GoogleParams,
]):

    @property
    @override
    def format(self) -> GoogleFormat:
        return GoogleFormat(GoogleFormatConfig(**self._config_format))

    @property
    @override
    def client(self) -> GoogleClient:
        return GoogleClient(GoogleClientConfig(**self._config_client))


API = GoogleFacadeDeps
