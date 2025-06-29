
from typing import override

from anthropic.types import TextBlockParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.models import StateOptions

from chatio.core.format.options import ApiFormatOptions

from chatio.api.claude.params import ClaudeStateOptions
from chatio.api.claude.config import ClaudeConfig


def text_message(text: str) -> TextBlockParam:
    return {
        "type": "text",
        "text": text,
    }


class ClaudeFormatOptions(ApiFormatOptions[
    ClaudeStateOptions,
    ClaudeConfig,
]):

    def system_content(self, content: TextBlockParam | None) -> list[TextBlockParam] | NotGiven:
        if content is None:
            return NOT_GIVEN

        if self._config.options.use_cache:
            content.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return [content]

    @override
    def format(self, options: StateOptions) -> ClaudeStateOptions:

        text = None if options.system is None else text_message(options.system.text)
        _system = self.system_content(text)

        return ClaudeStateOptions(
            system=_system,
        )
