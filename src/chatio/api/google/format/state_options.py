
from typing import override

from google.genai.types import ContentDict

from chatio.core.models import SystemMessage
from chatio.core.models import ChatStateOptions

from chatio.core.format.state_options import ApiOptionsFormatterBase

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfigFormat

from .state_messages import message_text


# pylint: disable=too-few-public-methods
class GoogleOptionsFormatter(ApiOptionsFormatterBase[
    GoogleStateOptions,
    GoogleConfigFormat,
]):

    def _system_message(self, msg: SystemMessage | None) -> ContentDict | None:
        if msg is None:
            return None

        content = message_text(msg)
        return {
            "parts": [content],
        }

    @override
    def format(self, options: ChatStateOptions) -> GoogleStateOptions:
        return GoogleStateOptions(
            system=self._system_message(options.system),
        )
