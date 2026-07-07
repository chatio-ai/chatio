
from typing import override

from chatio.core.facade import ApiFacadeDeps


from .config import OpenAIFormatConfig
from .config import OpenAIClientConfig
from .params import OpenAIParams
from .format import OpenAIFormat
from .client import OpenAIClient


class OpenAIFacadeDeps(ApiFacadeDeps[
    OpenAIParams,
]):

    @property
    @override
    def format(self) -> OpenAIFormat:
        return OpenAIFormat(OpenAIFormatConfig(**self._config_format))

    @property
    @override
    def client(self) -> OpenAIClient:
        return OpenAIClient(OpenAIClientConfig(**self._config_client))


API = OpenAIFacadeDeps
