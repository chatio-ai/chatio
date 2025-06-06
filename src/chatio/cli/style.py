

class StyleWrap:
    def __init__(self, prefix, suffix, end=None, file=None):
        self.prefix = prefix
        self.suffix = suffix
        self.file = file
        self.end = end

    def __enter__(self):
        print(self.prefix, end="", flush=True, file=self.file)

    def __exit__(self, *exc_info):
        print(self.suffix, end=self.end, flush=True, file=self.file)


class Style:

    RESET = "\033[0m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    def __init__(self, prefix=None, suffix=None, color=None):
        reset = Style.RESET
        if color is None:
            color = reset

        if prefix is None:
            prefix = ""

        if suffix is None:
            suffix = ""

        self.prefix = color + prefix
        self.suffix = suffix + reset

    def wrap(self, end=None, file=None):
        return StyleWrap(self.prefix, self.suffix, end=end, file=file)


Empty = Style("", "", Style.RESET)
