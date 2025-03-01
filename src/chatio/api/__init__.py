
from ._common import ChatBase
from ._common import ChatConfig

from .claude import ClaudeChat
from .openai import OpenAIChat


def build_chat(*args, **kwargs):
    config = kwargs.setdefault('config', ChatConfig())
    model = kwargs.get('model')

    if model is not None:
        config.model = model
    if config.model is None:
        raise RuntimeError("no model specified!")

    api_type = config.api_type
    if not api_type:
        return OpenAIChat(*args, **kwargs)
    if api_type == 'openai':
        return OpenAIChat(*args, **kwargs)
    if api_type == 'claude':
        return ClaudeChat(*args, **kwargs)

    raise RuntimeError("api_type not supported: %s" % api_type)
