
from typing import override

from google.genai.types import ContentUnionDict

from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.format import ApiFormat

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.config import GoogleConfig

from .history import GoogleFormatHistory
from .options import GoogleFormatOptions
from .tooling import GoogleFormatTooling


class GoogleFormat(ApiFormat[
    ContentUnionDict,
    GoogleStateOptions,
    ToolListUnionDict | None,
    ToolConfigDict | None,
    GoogleConfig,
]):

    @property
    @override
    def _format_options(self) -> GoogleFormatOptions:
        return GoogleFormatOptions(self._config)

    @property
    @override
    def _format_history(self) -> GoogleFormatHistory:
        return GoogleFormatHistory(self._config)

    @property
    @override
    def _format_tooling(self) -> GoogleFormatTooling:
        return GoogleFormatTooling(self._config)
