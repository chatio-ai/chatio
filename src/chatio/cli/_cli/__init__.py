
import sys

from typing import Protocol


# pylint: disable=too-few-public-methods
class EntryPointFunc(Protocol):
    def __call__(self, *args: str) -> None:
        ...


# pylint: disable=too-few-public-methods
class EntryPoint(Protocol):
    def __call__(self) -> None:
        ...


def entry_point(func: EntryPointFunc) -> EntryPoint:
    return lambda: func(*sys.argv[1:])
