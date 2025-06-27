
from typing import override

from google.genai.types import ContentDict
from google.genai.types import PartDict

from chatio.core.models import ChatOptions
from chatio.core.models import SystemContent

from chatio.core.format.options import ApiFormatOptions

from chatio.api.google.params import GoogleParamsOptions
from chatio.api.google.config import GoogleConfig


class GoogleFormatOptions(ApiFormatOptions[
    PartDict,
    GoogleParamsOptions,
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
    def format(self, options: ChatOptions) -> GoogleParamsOptions:
        _options: GoogleParamsOptions = {}

        for option in options.values():
            match option:
                case SystemContent(text):
                    _options.update({'system': self.system_content(self.text_message(text))})
                case _:
                    pass

        return _options
