
from typing import override

from chatio.api.openai.config import OpenAIConfigClient
from chatio.api.openai import OpenAIFacadeDeps


from .client import CompatClient


class CompatFacadeDeps(OpenAIFacadeDeps):

    @property
    @override
    def client(self) -> CompatClient:
        return CompatClient(OpenAIConfigClient(**self._config_client))


API = CompatFacadeDeps
