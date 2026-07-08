
from google.genai.types import ContentDict

from chatio.core.models import SystemMessage

from .state_messages import message_text


# pylint: disable=too-few-public-methods
class GoogleOptionsFormat:

    def system_message(self, msg: SystemMessage | None) -> ContentDict | None:
        if not msg:
            return None

        content = message_text(msg)
        return {
            "parts": [content],
        }
