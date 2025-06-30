
from dataclasses import dataclass


@dataclass
class ApiConfigOptions:
    pass


@dataclass
class ApiConfig[ApiConfigOptionsT: ApiConfigOptions]:
    options: ApiConfigOptionsT

    api: str | None
    env_ns: str | None = None
    api_key: str | None = None
    base_url: str | None = None


@dataclass
class ModelConfig:
    vendor: str
    model: str

    config: dict


@dataclass
class StateConfig:
    system: str | None = None
    messages: list[str] | None = None


@dataclass
class ToolsConfig:
    tools: dict | None = None
    tool_choice_mode: str | None = None
    tool_choice_name: str | None = None
