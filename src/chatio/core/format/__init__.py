
from abc import ABC, abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.config import ApiConfigFormat
from chatio.core.params import ApiParams

from ._base import ApiFormatBase


# pylint: disable=too-few-public-methods
class ApiFormat[
    ApiConfigFormatT: ApiConfigFormat,
    ApiParamsT: ApiParams,
](ApiFormatBase[ApiConfigFormatT], ABC):

    @abstractmethod
    def format(self, state: ChatState, tools: ChatTools) -> ApiParamsT:
        ...
