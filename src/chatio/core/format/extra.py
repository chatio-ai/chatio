
from abc import ABC, abstractmethod

from chatio.core.models import ContentEntry

from chatio.core.params import ApiExtras


class ApiFormatExtra[
    ApiExtrasT: ApiExtras
](ABC):

    @abstractmethod
    def index(self) -> list[str]:
        ...

    @abstractmethod
    def build(self, extras: dict[str, ContentEntry | None]) -> ApiExtrasT:
        ...
