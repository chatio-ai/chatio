
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
