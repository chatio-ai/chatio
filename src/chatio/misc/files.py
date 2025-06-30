
import os

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


def vendor_config(vendor_path: str) -> ModelConfig:
    config = _vendor_config_parse(vendor_path)

    _vendor_path, _model_name, config_data = config

    config_vendor = config_data.setdefault('vendor', {})

    vendor_env_ns = config_vendor.get('env_ns')
    if vendor_env_ns is None:
        vendor_env_ns = _vendor_path.stem
    vendor_env_ns = vendor_env_ns.upper()

    config_vendor.setdefault('api_key', os.getenv(f"{vendor_env_ns}_API_KEY"))
    config_vendor.setdefault('base_url', os.getenv(f"{vendor_env_ns}_BASE_URL"))

    return ModelConfig(str(_vendor_path), str(_model_name), config_data)
