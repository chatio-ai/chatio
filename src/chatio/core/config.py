
from dataclasses import dataclass


@dataclass
class ApiConfigFormat:
    pass


@dataclass
class ApiConfigVendor:
    api: str | None = None
    env_ns: str | None = None
    api_key: str | None = None
    base_url: str | None = None


@dataclass
class ModelConfig:
    vendor: str
    model: str

    config: dict
