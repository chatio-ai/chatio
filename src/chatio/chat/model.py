
from chatio.core.facade import ApiFacade

from chatio.api.claude.facade import ClaudeFacade
from chatio.api.google.facade import GoogleFacade
from chatio.api.openai.facade import OpenAIFacade


def init_facade(config: dict) -> ApiFacade:

    api = config.get('api')
    match api:
        case 'claude':
            return ClaudeFacade(config)
        case 'google':
            return GoogleFacade(config)
        case 'openai':
            return OpenAIFacade(config)
        case str():
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
        case _:
            err_msg = "api is not specified"
            raise RuntimeError(err_msg)
