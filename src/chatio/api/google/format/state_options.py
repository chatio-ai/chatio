
from typing import override

from google.genai.types import ContentDict
from google.genai.types import PartDict

from chatio.core.models import ChatStateOptions

from chatio.core.format.state_options import ApiOptionsFormatterBase

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfigFormat


def message_text(text: str) -> PartDict:
    return {
        "text": text,
    }


# pylint: disable=too-few-public-methods
class GoogleOptionsFormatter(ApiOptionsFormatterBase[
    GoogleStateOptions,
    GoogleConfigFormat,
]):

    def _system_message(self, content: PartDict | None) -> ContentDict | None:
        if content is None:
            return None

        return {
            "parts": [content],
        }

    @override
    def format(self, options: ChatStateOptions) -> GoogleStateOptions:

        text = None if options.system is None else message_text(options.system.text)
        _system = self._system_message(text)

        return GoogleStateOptions(
            system=_system,
        )
