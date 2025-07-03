
from abc import ABC, abstractmethod

from chatio.core.models import ChatOptions

from chatio.core.params import ApiParamsOptions
from chatio.core.config import ApiConfig

from ._common import ApiFormatBase


class ApiFormatOptions[
    ApiParamsOptionsT: ApiParamsOptions,
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
    ABC,
):

    @abstractmethod
    def index(self) -> list[str]:
        ...

    @abstractmethod
    def format(self, options: ChatOptions) -> ApiParamsOptionsT:
        ...
