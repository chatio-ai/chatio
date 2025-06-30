
from chatio.core.config import ModelConfig
from chatio.core.client import ApiClient

from chatio.api.claude.client import ClaudeClient
from chatio.api.google.client import GoogleClient
from chatio.api.openai.client import OpenAIClient


def init_client(model: ModelConfig) -> ApiClient:

    api = model.config.get('vendor', {}).get('api')
    match api:
        case 'claude':
            return ClaudeClient(model.config)
        case 'google':
            return GoogleClient(model.config)
        case 'openai':
            return OpenAIClient(model.config)
        case _:
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
