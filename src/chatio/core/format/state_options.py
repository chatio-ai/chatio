
from abc import ABC, abstractmethod

from chatio.core.models import ChatStateOptions

from chatio.core.params import ApiStateOptions


# pylint: disable=too-few-public-methods
class ApiOptionsFormat[
    ApiStateOptionsT: ApiStateOptions,
](ABC):

    @abstractmethod
    def __call__(self, options: ChatStateOptions) -> ApiStateOptionsT:
        ...
