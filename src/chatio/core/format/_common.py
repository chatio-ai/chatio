
from chatio.core.config import ApiConfigFormat


class ApiFormatBase[
    ApiConfigFormatT: ApiConfigFormat,
]:

    def __init__(self, config: ApiConfigFormatT) -> None:
        self._config = config

    @property
    def config(self) -> ApiConfigFormatT:
        return self._config

    def __call__(self) -> None:
        return None
