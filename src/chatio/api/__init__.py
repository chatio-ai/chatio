
from ._common import ChatBase
from ._common import ChatConfig

from .claude import ClaudeChat
from .google import GoogleChat
from .openai import OpenAIChat


def build_chat(*args, **kwargs) -> ChatBase:
    config: ChatConfig | None = kwargs.setdefault('config')
    model = kwargs.get('model')

    if config is None:
        err_msg = "no config specified!"
        raise RuntimeError
    if model is not None:
        config.model = model
    if config.model is None:
        err_msg = "no model specified!"
        raise RuntimeError(err_msg)

    api_type = config.api_type
    if not api_type:
        return OpenAIChat(*args, **kwargs)
    if api_type == 'claude':
        return ClaudeChat(*args, **kwargs)
    if api_type == 'google':
        return GoogleChat(*args, **kwargs)
    if api_type == 'openai':
        return OpenAIChat(*args, **kwargs)

    err_msg = f"api_type not supported: {api_type}"
    raise RuntimeError(err_msg)
