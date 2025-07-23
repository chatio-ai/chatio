
import os

from collections.abc import Iterator

import httpx


def _log_request(request: httpx.Request) -> None:
    content = request.content.decode()
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    print(f"{request.method} {request.url}\n{headers}\n\n{content}\n\n")


def _log_response(response: httpx.Response) -> None:
    headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
    print(f"{response.http_version} {response.status_code}\n{headers}\n\n")


def _log_response_trace(response: httpx.Response) -> None:
    _log_response(response)
    if not isinstance(response.stream, httpx.SyncByteStream):
        raise TypeError

    _iter_bytes = response.iter_bytes

    def iter_bytes(chunk_size: int | None = None) -> Iterator[bytes]:
        for chunk in _iter_bytes(chunk_size):
            print(chunk.decode())
            yield chunk

    response.iter_bytes = iter_bytes  # type: ignore[method-assign]


def httpx_args() -> dict:
    args: dict[str, object] = {}

    if os.getenv("CHATIO_HTTPX_TRACE"):
        args.update({
            "event_hooks": {
                "request": [_log_request],
                "response": [_log_response_trace],
            },
        })
    if os.getenv("CHATIO_HTTPX_DEBUG"):
        args.update({
            "event_hooks": {
                "request": [_log_request],
                "response": [_log_response],
            },
        })

    if os.getenv("CHATIO_HTTPX_INSECURE"):
        args.update({
            "verify": False,
        })

    return args
