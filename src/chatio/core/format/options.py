
from abc import ABC, abstractmethod

from chatio.core.models import ChatOptions

from chatio.core.params import ApiParamsOptions
from chatio.core.config import ApiConfig

from ._common import ApiFormatBase


class ApiFormatOptions[
    TextMessageT,
    ApiParamsOptionsT: ApiParamsOptions,
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
    ABC,
):

    @abstractmethod
    def text_message(self, text: str) -> TextMessageT:
        ...

    @abstractmethod
    def format(self, options: ChatOptions) -> ApiParamsOptionsT:
        ...
