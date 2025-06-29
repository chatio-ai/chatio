
import pathlib
import tomllib


def vendor_config(vendor_name: str) -> dict:
    vendor_file = pathlib.Path("./vendors").joinpath(vendor_name + ".toml")

    with vendor_file.open('rb') as vendorfp:
        return tomllib.load(vendorfp)
