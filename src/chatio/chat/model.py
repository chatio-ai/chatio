
from chatio.core.client import ApiClient

from chatio.api.claude.client import ClaudeClient
from chatio.api.google.client import GoogleClient
from chatio.api.openai.client import OpenAIClient


def init_client(config: dict) -> ApiClient:

    api = config.get('api')
    match api:
        case 'claude':
            return ClaudeClient(config)
        case 'google':
            return GoogleClient(config)
        case 'openai':
            return OpenAIClient(config)
        case str():
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
        case _:
            err_msg = f"api is not specified"
            raise RuntimeError(err_msg)
