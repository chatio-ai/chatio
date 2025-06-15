
from abc import ABC, abstractmethod

from dataclasses import dataclass


from .format import ChatFormat
from .format import ToolChoice

from .client import ChatClient


@dataclass
class ApiConfig:
    api_cls: str | None
    api_url: str | None = None
    api_key: str | None = None

    options: dict | None = None


@dataclass
class ApiParams:
    pass


@dataclass
class ChatConfig:
    vendor: str
    model: str

    config: ApiConfig


@dataclass
class ToolConfig:
    tools: dict | None = None
    tool_choice: ToolChoice | None = None
    tool_choice_name: str | None = None


class ChatApi[
    SystemContent,
    MessageContent,
    TextMessage,
    ImageMessage,
    ToolDefinition,
    ToolDefinitions,
    ToolSelection,
](ABC):

    @property
    @abstractmethod
    def config(self) -> ChatConfig:
        ...

    @property
    @abstractmethod
    def format(self) -> ChatFormat[
        SystemContent,
        MessageContent,
        TextMessage,
        ImageMessage,
        ToolDefinition,
        ToolDefinitions,
        ToolSelection,
    ]:
        ...

    @property
    @abstractmethod
    def client(self) -> ChatClient[
        SystemContent,
        MessageContent,
        ToolDefinitions,
        ToolSelection,
    ]:
        ...
