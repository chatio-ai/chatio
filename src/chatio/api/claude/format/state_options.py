
from anthropic.types import TextBlockParam

from anthropic import Omit, omit


from chatio.core.models import SystemMessage

from .state_messages import message_text


# pylint: disable=too-few-public-methods
class ClaudeOptionsFormat:

    def __init__(self, *, use_cache: bool) -> None:
        self._use_cache = use_cache

    def system_message(self, msg: SystemMessage | None) -> list[TextBlockParam] | Omit:
        if not msg:
            return omit

        content = message_text(msg)

        if self._use_cache:
            content.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return [content]
