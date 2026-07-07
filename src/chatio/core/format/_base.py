
from chatio.core.config import ApiFormatConfig


# pylint: disable=too-few-public-methods
class ApiFormatBase[
    ApiFormatConfigT: ApiFormatConfig,
]:

    def __init__(self, config: ApiFormatConfigT) -> None:
        self._config = config
