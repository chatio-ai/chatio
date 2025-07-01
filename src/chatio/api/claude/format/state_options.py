
from typing import override

from anthropic.types import TextBlockParam

from anthropic import NotGiven, NOT_GIVEN


from chatio.core.models import SystemMessage
from chatio.core.models import ChatStateOptions

from chatio.core.format.state_options import ApiOptionsFormatterBase

from chatio.api.claude.params import ClaudeStateOptions
from chatio.api.claude.config import ClaudeConfigFormat

from .state_messages import message_text


# pylint: disable=too-few-public-methods
class ClaudeOptionsFormatter(ApiOptionsFormatterBase[
    ClaudeStateOptions,
    ClaudeConfigFormat,
]):

    def _system_message(self, msg: SystemMessage | None) -> list[TextBlockParam] | NotGiven:
        if msg is None:
            return NOT_GIVEN

        content = message_text(msg)

        if self._config.use_cache:
            content.update({
                "cache_control": {
                    "type": "ephemeral",
                },
            })

        return [content]

    @override
    def format(self, options: ChatStateOptions) -> ClaudeStateOptions:
        return ClaudeStateOptions(
            system=self._system_message(options.system),
        )
