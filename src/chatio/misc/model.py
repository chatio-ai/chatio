
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


def _vendor_config_merge(config_defaults: dict, config_override: dict) -> dict:

    config = config_defaults | config_override
    config['format'] = config_defaults.get('format', {}) | config_override.get('format', {})
    config['client'] = config_defaults.get('client', {}) | config_override.get('client', {})

    return config


def _vendor_config_setup(
        vendor_path: str, config_defaults: dict, config_override: dict) -> dict:

    config = _vendor_config_merge(config_defaults, config_override)

    vendor_env_ns = config.get('env_ns')
    if vendor_env_ns is None:
        vendor_env_ns = vendor_path.rpartition('/')[-1]
    vendor_env_ns = vendor_env_ns.upper()

    config['client'] = config.get('client')
    if config['client'] is None:
        config['client'] = {}

    config['client'].setdefault('api_key', os.getenv(f"{vendor_env_ns}_API_KEY"))
    config['client'].setdefault('base_url', os.getenv(f"{vendor_env_ns}_BASE_URL"))

    return config


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
    _config_override = os.environ.get(env_name)
    config_override = {}
    if _config_override is not None:
        config_override = json.loads(_config_override)

    _config_defaults = _vendor_config_parse(model_name)
    vendor_path, model_name, config_defaults = _config_defaults

    config = _vendor_config_setup(vendor_path, config_defaults, config_override)

    return ModelConfig(vendor_path, model_name, config)
