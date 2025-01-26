

class ToolBase:

    __desc__ = None

    __schema__ = None

    def __init__(self, desc=None):
        if desc:
            self.__desc__ = desc
