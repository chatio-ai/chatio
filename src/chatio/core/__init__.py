
from abc import ABC, abstractmethod

from .config import ApiConfig
from .params import ApiParams
from .format import ApiFormat
from .client import ApiClient


class ApiHelper[ApiParamsT: ApiParams](ABC):

    @property
    @abstractmethod
    def config(self) -> ApiConfig:
        ...

    @property
    @abstractmethod
    def params(self) -> ApiParamsT:
        ...

    @property
    @abstractmethod
    def format(self) -> ApiFormat:
        ...

    @property
    @abstractmethod
    def client(self) -> ApiClient[ApiParamsT]:
        ...
