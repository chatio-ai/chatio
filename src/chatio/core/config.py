
from dataclasses import dataclass


@dataclass
class ApiFormatConfig:
    pass


@dataclass
class ApiClientConfig:
    api_key: str | None = None
    base_url: str | None = None


@dataclass
class ApiConfig:
    api: str | None = None
    env_ns: str = ""

    client: ApiClientConfig | None = None
    format: ApiFormatConfig | None = None


@dataclass
class ModelConfig:
    vendor: str
    model: str

    config: dict
