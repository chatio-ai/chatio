
from typing import override

from chatio.core.models import ContentEntry

from chatio.core.format.options import ApiFormatOptions

from chatio.core.params import ApiParamsOptions
from chatio.api.claude.config import ClaudeConfig


class ClaudeFormatOptions(ApiFormatOptions[
    ApiParamsOptions,
    ClaudeConfig,
]):

    @override
    def index(self) -> list[str]:
        return []

    @override
    def format(self, options: dict[str, ContentEntry | None]) -> ApiParamsOptions:
        return ApiParamsOptions()
