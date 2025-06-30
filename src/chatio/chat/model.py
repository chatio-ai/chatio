
# from chatio.core.config import ApiConfigOptions
# from chatio.core.config import ApiConfig

from chatio.core.config import ModelConfig
from chatio.core.client import ApiClient

from chatio.api.claude.config import ClaudeConfigOptions
from chatio.api.claude.config import ClaudeConfig
from chatio.api.claude.client import ClaudeClient

from chatio.api.google.config import GoogleConfigOptions
from chatio.api.google.config import GoogleConfig
from chatio.api.google.client import GoogleClient

from chatio.api.openai.config import OpenAIConfigOptions
from chatio.api.openai.config import OpenAIConfig
from chatio.api.openai.client import OpenAIClient


def init_client(model: ModelConfig) -> ApiClient:

    config_vendor = model.config.pop('vendor')
    config_options = model.config.pop('options')

    # options: ApiConfigOptions
    # config: ApiConfig

    api = config_vendor.get('vendor').get('api')
    match api:
        case 'claude':
            options = ClaudeConfigOptions(**config_options)
            config = ClaudeConfig(**config_vendor, options=options)
            return ClaudeClient(config)
        case 'google':
            options = GoogleConfigOptions(**config_options)
            config = GoogleConfig(**config_vendor, options=options)
            return GoogleClient(config)
        case 'openai':
            options = OpenAIConfigOptions(**config_options)
            config = OpenAIConfig(**config_vendor, options=options)
            return OpenAIClient(config)
        case _:
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)
