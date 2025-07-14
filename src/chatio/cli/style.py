
from dataclasses import dataclass

from enum import StrEnum


class Color(StrEnum):

    CLEAR = "\033[39m"

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


@dataclass
class Style:

    RESET = "\033[0m"

    BOLD = "\033[1m"
    DIM = "\033[2m"
    NORMAL = "\033[22m"

    prefix: str
    suffix: str = f"{RESET}"


Empty = Style("")


@dataclass
class Theme:
    INPUT = ">>> "
    OUTPUT = "<<< "

    chunk_pri: Style
    chunk_sec: Style

    event_pri: Style
    event_sec: Style

    def __init__(self, direction: str | None = None, color: Color | None = None) -> None:
        if direction is None:
            direction = ""
        if color is None:
            color = Color.CLEAR

        self.chunk_pri = Style(f"{Style.NORMAL}{color}{direction}")
        self.chunk_sec = Style(f"{Style.DIM}{color}{direction}    ")

        self.event_pri = Style(f"{Style.NORMAL}{color}{direction}::: ")
        self.event_sec = Style(f"{Style.DIM}{color}{direction}{Style.RESET}::: ")


Input = Theme(direction=Theme.INPUT)

Model = Theme(direction=Theme.OUTPUT)
