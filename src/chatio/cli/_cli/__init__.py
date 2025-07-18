
import sys

import asyncio

from typing import Protocol


# pylint: disable=too-few-public-methods
class EntryPointFunc(Protocol):
    async def __call__(self, *args: str) -> int | None:
        ...


# pylint: disable=too-few-public-methods
class EntryPoint(Protocol):
    def __call__(self) -> int | None:
        ...


def entry_point(func: EntryPointFunc) -> EntryPoint:
    def _func() -> int | None:
        return asyncio.run(func(*sys.argv[1:]))

    if func.__module__ == '__main__':
        raise SystemExit(_func())

    return _func
