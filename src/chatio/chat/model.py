
from chatio.core.facade import ApiFacadeDeps
from chatio.core.facade import ApiFacade


def init_facade(config: dict) -> ApiFacade:
    return ApiFacade(_init_facade_deps(config))


# ruff: noqa: PLC0415
# pylint: disable=import-outside-toplevel
def _init_facade_deps(config: dict) -> ApiFacadeDeps:

    api = config.get('api')
    match api:
        case 'claude':
            from chatio.api.claude.facade import ClaudeFacadeDeps
            return ClaudeFacadeDeps(config)
        case 'google':
            from chatio.api.google.facade import GoogleFacadeDeps
            return GoogleFacadeDeps(config)
        case 'openai':
            from chatio.api.openai.facade import OpenAIFacadeDeps
            return OpenAIFacadeDeps(config)
        case 'compat':
            from chatio.api.compat.facade import CompatFacadeDeps
            return CompatFacadeDeps(config)
        case str():
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
        case _:
            err_msg = "api is not specified"
            raise RuntimeError(err_msg)
