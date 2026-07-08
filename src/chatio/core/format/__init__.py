
from abc import ABC, abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiParams


# pylint: disable=too-few-public-methods
class ApiFormat[ApiParamsT: ApiParams](ABC):

    @abstractmethod
    def __call__(self, state: ChatState, tools: ChatTools) -> ApiParamsT:
        ...
