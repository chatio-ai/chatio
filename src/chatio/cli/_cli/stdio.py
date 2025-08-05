
import re

from types import TracebackType

from typing import TextIO

from .style import Style


class StyleWrap:

    def __init__(
        self, style: Style, end: str | None = None,
        file: TextIO | None = None, *, prompt: bool = False,
    ) -> None:
        self.style = style
        self.file = file
        self.end = end
        self.prompt = prompt

    def __enter__(self) -> str:
        if self.prompt:
            return re.sub('\033\\[[0-9;]*m', '\001\\g<0>\002', self.style.prefix)

        print(self.style.prefix, end="", flush=True, file=self.file)
        return ""

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        print(self.style.suffix, end=self.end, flush=True, file=self.file)


def _wrap_print(style: Style, end: str | None = None, file: TextIO | None = None) -> StyleWrap:
    return StyleWrap(style, end=end, file=file)


def _wrap_input(style: Style, end: str | None = None, file: TextIO | None = None) -> StyleWrap:
    return StyleWrap(style, end=end, file=file, prompt=True)
