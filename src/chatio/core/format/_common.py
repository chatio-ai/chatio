
from chatio.core.config import ApiConfig


class ApiFormatBase[
    ApiConfigT: ApiConfig,
]:

    def __init__(self, config: ApiConfigT) -> None:
        self._config = config

    @property
    def config(self) -> ApiConfigT:
        return self._config

    def __call__(self) -> None:
        return None
