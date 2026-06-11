
from importlib import import_module

import chatio.api

from chatio.core.config import ApiConfigFormat
from chatio.core.params import ApiParams

from chatio.core.facade import ApiFacadeDeps
from chatio.core.facade import ApiFacade


def init_facade(config: dict) -> ApiFacade[ApiConfigFormat, ApiParams]:
    api = config.get('api')
    if not api:
        err_msg = "api is not specified"
        raise RuntimeError(err_msg)

    cls = _init_facade_deps(api)
    return ApiFacade(cls(config))


def _init_facade_deps(api: str) -> type[ApiFacadeDeps[ApiConfigFormat, ApiParams]]:
    cls: type[ApiFacadeDeps[ApiConfigFormat, ApiParams]] = \
        import_module(f'.{api}', package=chatio.api.__name__).API
    return cls
