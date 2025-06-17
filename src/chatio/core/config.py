
from abc import ABC, abstractmethod

from dataclasses import dataclass


from .format import ApiFormat
from .client import ApiClient


@dataclass
class ApiTuning:
    pass


@dataclass
class ApiConfig[ApiTuningT: ApiTuning]:
    options: ApiTuningT

    api_cls: str | None
    api_url: str | None = None
    api_key: str | None = None


@dataclass
class ModelConfig:
    vendor: str
    model: str


@dataclass
class StateConfig:
    system: str | None = None
    messages: list[str] | None = None


@dataclass
class ToolsConfig:
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
