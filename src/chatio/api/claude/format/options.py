
from typing import override

from anthropic.types import TextBlockParam

from chatio.core.models import StateOptions

from chatio.core.format.options import ApiFormatOptions

from chatio.api.claude.params import ClaudeStateOptions
from chatio.api.claude.config import ClaudeConfig


class ClaudeFormatOptions(ApiFormatOptions[
    TextBlockParam,
    ClaudeStateOptions,
    ClaudeConfig,
]):

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
    def format(self, options: StateOptions) -> ClaudeStateOptions:
        system = None if options.system is None \
            else self.system_content(self.text_message(options.system.text))

        return ClaudeStateOptions(
            system=system,
        )
