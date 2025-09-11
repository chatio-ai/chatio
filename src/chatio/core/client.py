
from abc import ABC, abstractmethod

from .object import Closeable

from .params import ApiParams
from .stream import ApiStream


class ApiClient[
    ApiParamsT: ApiParams,
](Closeable, ABC):

    @abstractmethod
    def iterate_model_events(self, model: str, params: ApiParamsT) -> ApiStream:
        ...

    @abstractmethod
    async def count_message_tokens(self, model: str, params: ApiParamsT) -> int:
        ...
