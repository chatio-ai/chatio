
from collections.abc import Mapping


class ToolBase:

    __desc__: str | None = None

    __schema__: Mapping | None = None

    def __init__(self, desc=None):
        if desc is None:
            desc = self.__desc__
        self.desc = desc
        self.schema = self.__schema__
