
import time

from collections.abc import Iterator

from contextlib import contextmanager


@contextmanager
def timeit(name: str) -> Iterator[None]:
    begin = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f'{name}: {end - begin}')
