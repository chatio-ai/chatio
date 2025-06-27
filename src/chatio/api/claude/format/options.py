
from typing import override

from anthropic.types import TextBlockParam

from chatio.core.models import ChatOptions
from chatio.core.models import SystemContent

from chatio.core.format.options import ApiFormatOptions

from chatio.api.claude.params import ClaudeParamsOptions
from chatio.api.claude.config import ClaudeConfig


class ClaudeFormatOptions(ApiFormatOptions[
    TextBlockParam,
    ClaudeParamsOptions,
    ClaudeConfig,
]):

    @override
    def text_message(self, text: str) -> TextBlockParam:
        return {
            "type": "text",
            "text": text,
        }

    def system_content(self, content: TextBlockParam) -> TextBlockParam:
        if self._config.options.use_cache:
            content.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return content

    @override
    def format(self, options: ChatOptions) -> ClaudeParamsOptions:
        _options = ClaudeParamsOptions()

        for option in options.values():
            match option:
                case SystemContent(text):
                    _options.system = self.system_content(self.text_message(text))
                case _:
                    pass

        return _options
