
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import ChatStateOptions

from chatio.core.params import ApiStateOptions
from chatio.core.config import ApiConfigFormat

from ._base import ApiFormatBase


# pylint: disable=too-few-public-methods
class ApiOptionsFormatterBase[
    ApiStateOptionsT: ApiStateOptions,
    ApiConfigFormatT: ApiConfigFormat,
](ApiFormatBase[ApiConfigFormatT], ABC):

    @abstractmethod
    def format(self, options: ChatStateOptions) -> ApiStateOptionsT:
        ...


# pylint: disable=too-few-public-methods
class ApiOptionsFormatter[ApiStateOptionsT: ApiStateOptions](Protocol):

    @abstractmethod
    def format(self, options: ChatStateOptions) -> ApiStateOptionsT:
        ...
