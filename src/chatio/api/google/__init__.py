
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

    @property
    @override
    def format(self) -> GoogleFormat:
        return GoogleFormat(GoogleConfigFormat(**self._config_format))

    @property
    @override
    def client(self) -> GoogleClient:
        return GoogleClient(GoogleConfigClient(**self._config_client))


API = GoogleFacadeDeps
