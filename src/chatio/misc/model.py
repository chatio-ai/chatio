
import os
import json

import pathlib
import tomllib

from chatio.core.config import ModelConfig


def _vendor_config_parse(model_name: str) -> tuple[str, str, dict]:
    config = None

    vendors_dir = pathlib.Path('./vendors').resolve()
    vendor_path = pathlib.Path()
    while model_name:
        vendor_path_part, _, model_name = model_name.partition('/')
        vendor_path = vendor_path.joinpath(vendor_path_part)

        config_file = vendors_dir.joinpath(vendor_path).with_suffix('.toml').resolve()

        try:
            with config_file.open('rb') as vendorfp:
                config_data = tomllib.load(vendorfp)

            _vendor_path = config_file.relative_to(vendors_dir).with_suffix("")
            config = str(_vendor_path), model_name, config_data
        except FileNotFoundError:
            if config:
                break

    if config is None:
        raise FileNotFoundError

    return config


def vendor_config(model_name: str, config_override: dict | None = None) -> ModelConfig:
    if config_override is None:
        config_override = {}

    config_client_override = config_override.pop('client', {})
    config_format_override = config_override.pop('format', {})

    config = _vendor_config_parse(model_name)

    _vendor_path, _model_name, _config = config
    _config.update(config_override)

    vendor_env_ns = _config.get('env_ns')
    if vendor_env_ns is None:
        vendor_env_ns = _vendor_path.rpartition('/')[-1]
    vendor_env_ns = vendor_env_ns.upper()

    _config_client = _config.setdefault('client', {})
    _config_client.setdefault('api_key', os.getenv(f"{vendor_env_ns}_API_KEY"))
    _config_client.setdefault('base_url', os.getenv(f"{vendor_env_ns}_BASE_URL"))
    _config_client.update(config_client_override)

    _config_format = _config.setdefault('format', {})
    _config_format.update(config_format_override)

    return ModelConfig(_vendor_path, _model_name, _config)


def build_model(model_name: str | None = None, env_ns: str | None = None) -> ModelConfig:
    _env_ns = "CHATIO"
    if env_ns is not None:
        _env_ns = _env_ns + "_" + env_ns

    if model_name is None:
        env_name = f"{_env_ns}_MODEL_NAME"
        model_name = os.environ.get(env_name)
        if model_name is None:
            err_msg = f"Configure {env_name}!"
            raise RuntimeError(err_msg)

    env_name = f"{_env_ns}_VENDOR_CONFIG"
    config_override = os.environ.get(env_name)
    _config_override = json.loads(config_override) if config_override is not None else None

    return vendor_config(model_name, _config_override)
