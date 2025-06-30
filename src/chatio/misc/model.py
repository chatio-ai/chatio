
import os
import json

import pathlib
import tomllib

from chatio.core.config import ModelConfig


def _vendor_config_parse(vendor_path: str) -> tuple[pathlib.Path, pathlib.Path, dict]:
    _tmp_vendor_path = pathlib.Path(vendor_path)

    _vendors_dir = pathlib.Path("./vendors").resolve()
    for _vendor_path in _tmp_vendor_path.parents[:-1]:
        config_file = _vendors_dir.joinpath(_vendor_path.with_suffix('.toml')).resolve()

        try:
            with config_file.open('rb') as vendorfp:
                config_data = tomllib.load(vendorfp)
        except FileNotFoundError:
            continue
        else:
            _model_path = _tmp_vendor_path.relative_to(_vendor_path)
            _vendor_path = config_file.relative_to(_vendors_dir).with_suffix("")
            return _vendor_path, _model_path, config_data

    raise FileNotFoundError


def vendor_config(vendor_path: str, config_options: dict | None = None) -> ModelConfig:
    config = _vendor_config_parse(vendor_path)

    _vendor_path, _model_name, config_data = config

    _config_vendor = config_data.setdefault('vendor', {})

    vendor_env_ns = _config_vendor.get('env_ns')
    if vendor_env_ns is None:
        vendor_env_ns = _vendor_path.stem
    vendor_env_ns = vendor_env_ns.upper()

    _config_vendor.setdefault('api_key', os.getenv(f"{vendor_env_ns}_API_KEY"))
    _config_vendor.setdefault('base_url', os.getenv(f"{vendor_env_ns}_BASE_URL"))

    if config_options is None:
        config_options = {}
    _config_options = config_data.setdefault('options', {})
    _config_options.update(config_options)

    return ModelConfig(str(_vendor_path), str(_model_name), config_data)


def build_model(model_name: str | None = None, env_ns: str | None = None) -> ModelConfig:
    if env_ns is None:
        env_ns = ""

    if model_name is None:
        env_name = f"{env_ns}CHATIO_MODEL_NAME"
        model_name = os.environ.get(env_name)
        if model_name is None:
            err_msg = f"Configure {env_name}!"
            raise RuntimeError(err_msg)

    env_name = "f{env_ns}CHATIO_API_OPTIONS"
    config_options = os.environ.get(env_name)
    _config_options = json.loads(config_options) if config_options is not None else None

    return vendor_config(model_name, _config_options)
