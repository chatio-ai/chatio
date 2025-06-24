
from abc import ABC, abstractmethod

from .config import ApiConfig
from .format import ApiFormat
from .client import ApiClient


class ApiHelper[
    SystemContent,
    MessageContent,
    PredictionContent,
    TextMessage,
    ImageMessage,
    ToolDefinition,
    ToolDefinitions,
    ToolSelection,
](ABC):

    @property
    @abstractmethod
    def config(self) -> ApiConfig:
        ...

    @property
    @abstractmethod
    def format(self) -> ApiFormat[
        SystemContent,
        MessageContent,
        PredictionContent,
        TextMessage,
        ImageMessage,
        ToolDefinition,
        ToolDefinitions,
        ToolSelection,
    ]:
        ...

    @property
    @abstractmethod
    def client(self) -> ApiClient[
        SystemContent,
        MessageContent,
        PredictionContent,
        ToolDefinitions,
        ToolSelection,
    ]:
        ...
