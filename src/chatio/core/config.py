
from abc import ABC, abstractmethod

from dataclasses import dataclass


from .format import ChatFormat
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
    tool_choice: str | None = None
    tool_choice_name: str | None = None


class ChatApi[SystemContent, MessageContent, TextMessage, ImageMessage](ABC):

    @property
    @abstractmethod
    def config(self) -> ChatConfig:
        ...

    @property
    @abstractmethod
    def format(self) -> ChatFormat[SystemContent, MessageContent, TextMessage, ImageMessage]:
        ...

    @property
    @abstractmethod
    def client(self) -> ChatClient[SystemContent, MessageContent]:
        ...
