
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import OpenAIConfigFormat
from .config import OpenAIConfigClient
from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIFacadeDeps(ApiFacadeDeps[
    OpenAIConfigFormat,
    OpenAIParams,
]):

    @property
    @override
    def format(self) -> OpenAIFormat:
        return OpenAIFormat(OpenAIConfigFormat(**self._config_format))

    @property
    @override
    def client(self) -> OpenAIClient:
        return OpenAIClient(OpenAIConfigClient(**self._config_client))
