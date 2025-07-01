
from dataclasses import dataclass


@dataclass
class ApiConfigFormat:
    pass


@dataclass
class ApiConfigClient:
    api_key: str | None = None
    base_url: str | None = None


@dataclass
class ApiConfig:
    api: str | None = None
    env_ns: str | None = None

    client: ApiConfigClient | None = None
    format: ApiConfigFormat | None = None


@dataclass
class ModelConfig:
    vendor: str
    model: str

    config: dict
