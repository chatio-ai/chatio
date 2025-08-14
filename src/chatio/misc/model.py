
import os
import json

import pathlib
import tomllib

from importlib import resources

from chatio.core.config import ModelConfig


def _vendor_config_parse_dir(vendors_root: pathlib.Path, model_name: str) -> ModelConfig | None:
    config = None

    vendors_dir = vendors_root.resolve()
    vendor_path = pathlib.Path()
    while model_name:
        vendor_path_part, _, model_name = model_name.partition('/')
        vendor_path = vendor_path.joinpath(vendor_path_part)

        config_file = vendors_dir.joinpath(vendor_path).with_suffix('.toml').resolve()

        try:
            with config_file.open('rb') as vendorfp:
                config_data = tomllib.load(vendorfp)

            vendor_name = str(config_file.relative_to(vendors_dir).with_suffix(""))
            config = ModelConfig(vendor_name, model_name, config_data)
        except FileNotFoundError:
            if config is not None:
                break

    return config


def _vendor_config_parse(model_name: str) -> ModelConfig | None:
    vendors_dirs = os.environ.get('CHATIO_VENDORS_PATH')
    if vendors_dirs is None:
        vendors_dirs = ""

    for vendors_dir in vendors_dirs.split(':'):
        vendors_dir_path = pathlib.Path(vendors_dir)
        config = _vendor_config_parse_dir(vendors_dir_path, model_name)
        if config is not None:
            return config

    vendors_res = resources.files('chatio').joinpath('share/vendors')
    with resources.as_file(vendors_res) as vendors_res_path:
        return _vendor_config_parse_dir(vendors_res_path, model_name)


def _vendor_config_fetch(model_name: str) -> ModelConfig:
    config = _vendor_config_parse(model_name)
    if config is None:
        raise FileNotFoundError

    config_ref = config.config.pop('ref', None)
    if config_ref is None:
        return config
    if config.config:
        raise ValueError

    if not config_ref.startswith('/'):
        config_ref = config.vendor.rpartition('/')[0] + '/' + config_ref

    return _vendor_config_fetch(config_ref + '/' + config.model)


def _vendor_config_merge(config_defaults: dict, config_override: dict) -> dict:

    config = config_defaults | config_override
    config['format'] = config_defaults.get('format', {}) | config_override.get('format', {})
    config['client'] = config_defaults.get('client', {}) | config_override.get('client', {})

    return config


def _vendor_config_setup(config: ModelConfig, overrides: dict) -> ModelConfig:

    config.config = _vendor_config_merge(config.config, overrides)

    vendor_env_ns = config.config.get('env_ns')
    if vendor_env_ns is None:
        vendor_env_ns = config.vendor.rpartition('/')[-1]
    vendor_env_ns = vendor_env_ns.upper()

    config.config['client'] = config.config.get('client')
    if config.config['client'] is None:
        config.config['client'] = {}

    config.config['client'].setdefault('api_key', os.getenv(f"{vendor_env_ns}_API_KEY"))
    config.config['client'].setdefault('base_url', os.getenv(f"{vendor_env_ns}_BASE_URL"))

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
    _overrides = os.environ.get(env_name)
    overrides = {}
    if _overrides is not None:
        overrides = json.loads(_overrides)

    config = _vendor_config_fetch(model_name)
    return _vendor_config_setup(config, overrides)
