
from abc import ABC, abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools


# pylint: disable=too-few-public-methods
class ApiFormat[
    ApiParamsT,
](ABC):

    @abstractmethod
    def __call__(self, state: ChatState, tools: ChatTools) -> ApiParamsT:
        ...
