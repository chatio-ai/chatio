
from abc import ABC, abstractmethod

from dataclasses import dataclass


from .format import ApiFormat
from .client import ApiClient


@dataclass
class ApiTuning:
    pass


@dataclass
class ApiConfig[ApiTuningT: ApiTuning]:
    api: ApiTuningT

    cls: str | None
    url: str | None = None
    key: str | None = None


@dataclass
class ModelConfig:
    vendor: str
    model: str


@dataclass
class ToolConfig:
    tools: dict | None = None
    tool_choice_mode: str | None = None
    tool_choice_name: str | None = None


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
    def config(self) -> ModelConfig:
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
