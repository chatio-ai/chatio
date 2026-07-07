
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import ChatStateOptions

from chatio.core.params import ApiStateOptions


# pylint: disable=too-few-public-methods
class ApiOptionsFormatterBase[
    ApiStateOptionsT: ApiStateOptions,
](ABC):

    @abstractmethod
    def format(self, options: ChatStateOptions) -> ApiStateOptionsT:
        ...


# pylint: disable=too-few-public-methods
class ApiOptionsFormatter[ApiStateOptionsT: ApiStateOptions](Protocol):

    @abstractmethod
    def format(self, options: ChatStateOptions) -> ApiStateOptionsT:
        ...
