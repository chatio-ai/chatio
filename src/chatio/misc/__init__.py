
import os
import json
import logging

from chatio.core.config import ModelConfig

from chatio.core.config import ApiConfigOptions
from chatio.core.config import ApiConfig

from chatio.api.claude.config import ClaudeConfigOptions
from chatio.api.claude.config import ClaudeConfig
from chatio.api.claude.client import ClaudeClient

from chatio.api.google.config import GoogleConfigOptions
from chatio.api.google.config import GoogleConfig
from chatio.api.google.client import GoogleClient

from chatio.api.openai.config import OpenAIConfigOptions
from chatio.api.openai.config import OpenAIConfig
from chatio.api.openai.client import OpenAIClient

from chatio.chat import Chat

from chatio.chat.state import ChatState


from .files import vendor_config
from .tools import build_tools


def setup_logging() -> None:
    logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')
    logging.getLogger('chatio.api').setLevel(logging.INFO)


def build_model(model_name: str | None = None, env_ns: str | None = None) -> ModelConfig:
    if env_ns is None:
        env_ns = ""

    if model_name is None:
        env_name = f"{env_ns}CHATIO_MODEL_NAME"
        model_name = os.environ.get(env_name)
        if model_name is None:
            err_msg = f"Configure {env_name}!"
            raise RuntimeError(err_msg)

    env_name = "f{env_ns}CHATIO_API_OPTIONS"
    config_options = os.environ.get(env_name)
    _config_options = json.loads(config_options) if config_options is not None else None

    return vendor_config(model_name, _config_options)


def build_chat(
    prompt: str | None = None,
    messages: list[str] | None = None,
    tools: str | None = None,
    model: str | None = None,
) -> Chat:

    _tools = build_tools(tools)
    _state = build_state(prompt, messages)
    _model = build_model(model)

    config_vendor = _model.config.pop('vendor')
    config_options = _model.config.pop('options', {})

    options: ApiConfigOptions
    config: ApiConfig

    api = config_vendor.get('api')
    match api:
        case 'claude':
            options = ClaudeConfigOptions(**config_options)
            config = ClaudeConfig(**config_vendor, options=options)
            return Chat(ClaudeClient(config), _model, _state, _tools)
        case 'google':
            options = GoogleConfigOptions(**config_options)
            config = GoogleConfig(**config_vendor, options=options)
            return Chat(GoogleClient(config), _model, _state, _tools)
        case 'openai':
            options = OpenAIConfigOptions(**config_options)
            config = OpenAIConfig(**config_vendor, options=options)
            return Chat(OpenAIClient(config), _model, _state, _tools)
        case _:
            err_msg = f"api is not supported: {api}"
            raise RuntimeError(err_msg)


def build_state(prompt: str | None = None, messages: list[str] | None = None) -> ChatState:
    return ChatState(prompt, messages)
