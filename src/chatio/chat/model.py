
from chatio.core.facade import ApiFacadeDeps
from chatio.core.facade import ApiFacade

from chatio.api.claude.facade import ClaudeFacadeDeps
from chatio.api.google.facade import GoogleFacadeDeps
from chatio.api.openai.facade import OpenAIFacadeDeps
from chatio.api.compat.facade import CompatFacadeDeps


def _init_facade_deps(config: dict) -> ApiFacadeDeps:

    api = config.get('api')
    match api:
        case 'claude':
            return ClaudeFacadeDeps(config)
        case 'google':
            return GoogleFacadeDeps(config)
        case 'openai':
            return OpenAIFacadeDeps(config)
        case 'compat':
            return CompatFacadeDeps(config)
        case str():
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
        case _:
            err_msg = "api is not specified"
            raise RuntimeError(err_msg)


def init_facade(config: dict) -> ApiFacade:
    return ApiFacade(_init_facade_deps(config))
