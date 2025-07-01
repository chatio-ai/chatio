
from typing import override

from google.genai.types import ContentUnionDict

from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.format import ApiFormat

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfigFormat

from .state_messages import GoogleMessagesFormatter
from .state_options import GoogleOptionsFormatter
from .tools import GoogleToolsFormatter


# pylint: disable=too-few-public-methods
class GoogleFormat(ApiFormat[
    ContentUnionDict,
    GoogleStateOptions,
    ToolListUnionDict | None,
    ToolConfigDict | None,
    GoogleConfigFormat,
]):

    @property
    @override
    def _messages_formatter(self) -> GoogleMessagesFormatter:
        return GoogleMessagesFormatter(self._config)

    @property
    @override
    def _options_formatter(self) -> GoogleOptionsFormatter:
        return GoogleOptionsFormatter(self._config)

    @property
    @override
    def _tools_formatter(self) -> GoogleToolsFormatter:
        return GoogleToolsFormatter(self._config)
