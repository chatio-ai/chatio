
from typing import override

from google.genai.types import ContentDict
from google.genai.types import PartDict

from chatio.core.models import StateOptions

from chatio.core.format.options import ApiFormatOptions

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfig


class GoogleFormatOptions(ApiFormatOptions[
    PartDict,
    GoogleStateOptions,
    GoogleConfig,
]):

    @override
    def text_message(self, text: str) -> PartDict:
        return {
            "text": text,
        }

    def system_content(self, content: PartDict) -> ContentDict:
        return {
            "parts": [content],
        }

    @override
    def format(self, options: StateOptions) -> GoogleStateOptions:
        system = None if options.system is None \
            else self.system_content(self.text_message(options.system.text))

        return GoogleStateOptions(
            system=system,
        )
