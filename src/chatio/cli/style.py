

class StyleWrap:
    def __init__(self, style, end=None, file=None, *, prompt=False):
        self.style = style
        self.file = file
        self.end = end
        self.prompt = prompt

    def __enter__(self):
        print(self.style.color, end="", flush=True, file=self.file)
        if self.prompt:
            return self.style.prefix

        print(self.style.prefix, end="", flush=True, file=self.file)
        return ""

    def __exit__(self, *exc_info):
        print(self.style.suffix, end="", flush=True, file=self.file)
        print(self.style.reset, end=self.end, flush=True, file=self.file)


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
        self.conf(prefix, suffix, color)

    def conf(self, prefix=None, suffix=None, color=None):
        self.reset = Style.RESET
        if color is None:
            color = self.reset
        self.color = color

        if prefix is None:
            prefix = ""

        if suffix is None:
            suffix = ""

        self.prefix = prefix
        self.suffix = suffix

    def wrap_print(self, end=None, file=None):
        return StyleWrap(self, end=end, file=file)

    def wrap_input(self, end=None, file=None):
        return StyleWrap(self, end=end, file=file, prompt=True)


Empty = Style("", "", Style.RESET)
