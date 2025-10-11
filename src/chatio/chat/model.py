
from importlib import import_module

import chatio.api

from chatio.core.facade import ApiFacadeDeps
from chatio.core.facade import ApiFacade


def init_facade(config: dict) -> ApiFacade:
    return ApiFacade(_init_facade_deps(config))


def _init_facade_deps(config: dict) -> ApiFacadeDeps:

    api = config.get('api')
    if not api:
        err_msg = "api is not specified"
        raise RuntimeError(err_msg)

    return import_module(f'.{api}', package=chatio.api.__name__).API(config)
