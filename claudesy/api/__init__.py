
from ._common import ChatBase
from ._common import ChatConfig

from .claude import ClaudeChat
from .openai import OpenAIChat


def build(self,
          system=None,
          messages=None,
          tools=None,
          tool_choice=None,
          tool_choice_name=None,
          model=None,
          config: ChatConfig = None, **kwargs):
    api_type = config.api_type

    if not api_type:
        return OpenAIChat(config=config, **kwargs)
    if api_type == 'openai':
        return OpenAIChat(config=config, **kwargs)
    if api_type == 'claude':
        return ClaudeChat(config=config)

    raise RuntimeError("api_type not supported: %s" % api_type)
