
from typing import override

from chatio.core.models import ChatOptions

from chatio.core.format.options import ApiFormatOptions

from chatio.core.params import ApiParamsOptions
from chatio.api.google.config import GoogleConfig


class GoogleFormatOptions(ApiFormatOptions[
    ApiParamsOptions,
    GoogleConfig,
]):

    @override
    def index(self) -> list[str]:
        return []

    @override
    def format(self, options: ChatOptions) -> ApiParamsOptions:
        return ApiParamsOptions()
