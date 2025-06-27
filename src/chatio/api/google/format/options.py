
from typing import override

from chatio.core.models import ContentEntry

from chatio.core.format.options import ApiFormatOptions

from chatio.core.params import ApiExtras
from chatio.api.google.config import GoogleConfig


class GoogleFormatOptions(ApiFormatOptions[
    ApiExtras,
    GoogleConfig,
]):

    @override
    def index(self) -> list[str]:
        return []

    @override
    def build(self, extras: dict[str, ContentEntry | None]) -> ApiExtras:
        return ApiExtras()
