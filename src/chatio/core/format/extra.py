
from abc import ABC, abstractmethod

from chatio.core.models import ContentEntry

from chatio.core.params import ApiExtras
from chatio.core.config import ApiConfig


class ApiFormatExtra[
    ApiExtrasT: ApiExtras,
    ApiConfigT: ApiConfig,
](ABC):

    def __init__(self, config: ApiConfigT) -> None:
        self._config = config

    @abstractmethod
    def index(self) -> list[str]:
        ...

    @abstractmethod
    def build(self, extras: dict[str, ContentEntry | None]) -> ApiExtrasT:
        ...
