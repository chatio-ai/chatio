
from ._common import ChatBase
from ._common import ChatConfig

from .claude import ClaudeChat
from .google import GoogleChat
from .openai import OpenAIChat


def build_chat(*args, **kwargs) -> ChatBase:
    config: ChatConfig | None = kwargs.get('config')

    if config is None:
        err_msg = "no config specified!"
        raise RuntimeError
    if config.model is None:
        err_msg = "no model specified!"
        raise RuntimeError(err_msg)

    match config.config.api_cls:
        case 'claude':
            return ClaudeChat(*args, **kwargs)
        case 'google':
            return GoogleChat(*args, **kwargs)
        case 'openai':
            return OpenAIChat(*args, **kwargs)
        case _:
            err_msg = f"api_cls not supported: {config.config.api_cls}"
            raise RuntimeError(err_msg)
