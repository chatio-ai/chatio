
from typing import override

from chatio.api.openai.facade import OpenAIFacadeDeps
from chatio.api.openai.config import OpenAIConfigClient


from .client import CompatClient


class CompatFacadeDeps(OpenAIFacadeDeps):

    @property
    @override
    def client(self) -> CompatClient:
        return CompatClient(OpenAIConfigClient(**self._config_client))
