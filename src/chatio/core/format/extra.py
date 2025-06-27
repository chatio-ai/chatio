
from abc import ABC, abstractmethod

from chatio.core.models import ContentEntry

from chatio.core.params import ApiExtras
from chatio.core.config import ApiConfig

from ._common import ApiFormatBase


class ApiFormatExtra[
    ApiExtrasT: ApiExtras,
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
    ABC,
):

    @abstractmethod
    def index(self) -> list[str]:
        ...

    @abstractmethod
    def build(self, extras: dict[str, ContentEntry | None]) -> ApiExtrasT:
        ...
