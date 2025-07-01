
from typing import override

from google.genai.types import ContentUnionDict

from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.format import ApiFormat

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfigFormat

from .history import GoogleHistoryFormatter
from .options import GoogleOptionsFormatter
from .tooling import GoogleToolingFormatter


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
    def _history_formatter(self) -> GoogleHistoryFormatter:
        return GoogleHistoryFormatter(self._config)

    @property
    @override
    def _options_formatter(self) -> GoogleOptionsFormatter:
        return GoogleOptionsFormatter(self._config)

    @property
    @override
    def _tooling_formatter(self) -> GoogleToolingFormatter:
        return GoogleToolingFormatter(self._config)
