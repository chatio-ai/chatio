
from abc import ABC, abstractmethod

from chatio.core.models import StateOptions

from chatio.core.params import ApiStateOptions
from chatio.core.config import ApiConfig

from ._common import ApiFormatBase


class ApiFormatOptions[
    TextMessageT,
    ApiStateOptionsT: ApiStateOptions,
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
    ABC,
):

    @abstractmethod
    def text_message(self, text: str) -> TextMessageT:
        ...

    @abstractmethod
    def format(self, options: StateOptions) -> ApiStateOptionsT:
        ...
