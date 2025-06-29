
import os

import pathlib
import tomllib


def vendor_config(vendor_name: str) -> tuple[str, dict]:
    config_file = pathlib.Path("./vendors").joinpath(vendor_name).with_suffix('.toml').resolve()

    with config_file.open('rb') as vendorfp:
        config_data = tomllib.load(vendorfp)

    config_vendor = config_data.setdefault('vendor', {})

    vendor_name = config_file.stem
    vendor_env_ns = config_vendor.get('env_ns')
    if vendor_env_ns is None:
        vendor_env_ns = vendor_name
    vendor_env_ns = vendor_env_ns.upper()

    config_vendor.setdefault('api_key', os.getenv(f"{vendor_env_ns}_API_KEY"))
    config_vendor.setdefault('base_url', os.getenv(f"{vendor_env_ns}_BASE_URL"))

    return vendor_name, config_data
