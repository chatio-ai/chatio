
import os

from ..api._common import ChatConfig


def init_config():
    return ChatConfig(os.environ.get("CHATIO_PROVIDER_JSON", "./provider.json"))
