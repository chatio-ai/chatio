
from chatio.core.facade import ApiFacade
from chatio.core.facade import ApiFacadeDeps
from chatio.core.facade import ApiFacadeImpl

from chatio.api.claude.facade import ClaudeFacadeDeps
from chatio.api.google.facade import GoogleFacadeDeps
from chatio.api.openai.facade import OpenAIFacadeDeps


def _init_facade_deps(config: dict) -> ApiFacadeDeps:

    api = config.get('api')
    match api:
        case 'claude':
            return ClaudeFacadeDeps(config)
        case 'google':
            return GoogleFacadeDeps(config)
        case 'openai':
            return OpenAIFacadeDeps(config)
        case str():
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
        case _:
            err_msg = "api is not specified"
            raise RuntimeError(err_msg)


def init_facade(config: dict) -> ApiFacade:
    return ApiFacadeImpl(_init_facade_deps(config))
