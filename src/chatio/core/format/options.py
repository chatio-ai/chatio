
from abc import ABC, abstractmethod

from typing import Protocol

from chatio.core.models import StateOptions

from chatio.core.params import ApiStateOptions
from chatio.core.config import ApiConfig

from ._common import ApiFormatBase


# pylint: disable=too-few-public-methods
class ApiFormatOptions[
    TextMessageT,
    ApiStateOptionsT: ApiStateOptions,
    ApiConfigT: ApiConfig,
](
    ApiFormatBase[ApiConfigT],
    ABC,
):

    @abstractmethod
    def format(self, options: StateOptions) -> ApiStateOptionsT:
        ...


# pylint: disable=too-few-public-methods
class ApiFormatOptionsProto[ApiStateOptionsT: ApiStateOptions](Protocol):

    @abstractmethod
    def format(self, options: StateOptions) -> ApiStateOptionsT:
        ...
