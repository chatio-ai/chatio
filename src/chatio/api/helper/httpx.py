
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


class LoggedStream(httpx.SyncByteStream):
    def __init__(self, stream: httpx.SyncByteStream) -> None:
        self.stream = stream

    def __iter__(self) -> Iterator[bytes]:
        for chunk in self.stream:
            print(chunk.decode())
            yield chunk


def _log_response_trace(response: httpx.Response) -> None:
    _log_response(response)
    if not isinstance(response.stream, httpx.SyncByteStream):
        raise TypeError
    response.stream = LoggedStream(response.stream)


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
