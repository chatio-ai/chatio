
from typing import override

from google.genai.types import ContentDict
from google.genai.types import PartDict

from chatio.core.models import StateOptions

from chatio.core.format.state_options import ApiOptionsFormatterBase

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfigFormat


def text_message(text: str) -> PartDict:
    return {
        "text": text,
    }


# pylint: disable=too-few-public-methods
class GoogleOptionsFormatter(ApiOptionsFormatterBase[
    GoogleStateOptions,
    GoogleConfigFormat,
]):

    def _system_content(self, content: PartDict | None) -> ContentDict | None:
        if content is None:
            return None

        return {
            "parts": [content],
        }

    @override
    def format(self, options: StateOptions) -> GoogleStateOptions:

        text = None if options.system is None else text_message(options.system.text)
        _system = self._system_content(text)

        return GoogleStateOptions(
            system=_system,
        )
