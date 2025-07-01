
from chatio.core.config import ApiConfigFormat


# pylint: disable=too-few-public-methods
class ApiFormatBase[
    ApiConfigFormatT: ApiConfigFormat,
]:

    def __init__(self, config: ApiConfigFormatT) -> None:
        self._config = config
