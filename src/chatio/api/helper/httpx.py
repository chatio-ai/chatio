
import os

from collections.abc import Iterator

from typing import override

import httpx


class LoggingResponse(httpx.Response):

    @override
    def iter_bytes(self, chunk_size: int | None = None) -> Iterator[bytes]:
        buffer = bytearray()
        for chunk in super().iter_bytes(chunk_size):
            print(chunk.decode())
            buffer.extend(chunk)
            yield b""
        yield bytes(buffer)


class LoggingTransport(httpx.HTTPTransport):

    def __init__(self, *, verbose: bool = False) -> None:
        super().__init__()
        self.verbose = verbose

    def _log_request(self, request: httpx.Request) -> None:
        content = request.content.decode()
        headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
        print(f"{request.method} {request.url}\n{headers}\n\n{content}\n\n")

    def _log_response(self, response: httpx.Response) -> None:
        headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
        print(f"{response.http_version} {response.status_code}\n{headers}\n\n")

    @override
    def handle_request(self,
                       request: httpx.Request, **kwargs: object) -> httpx.Response:

        self._log_request(request)
        response = super().handle_request(request, **kwargs)
        self._log_response(response)

        if self.verbose:
            return LoggingResponse(
                status_code=response.status_code,
                headers=response.headers,
                stream=response.stream,
                extensions=response.extensions,
            )

        return response


def httpx_args() -> dict:
    args: dict[str, object] = {}

    if os.getenv("CHATIO_HTTPX_TRACE"):
        args.update({
            'transport': LoggingTransport(verbose=True),
        })
    if os.getenv("CHATIO_HTTPX_DEBUG"):
        args.update({
            'transport': LoggingTransport(verbose=False),
        })

    if os.getenv("CHATIO_HTTPX_INSECURE"):
        args.update({
            "verify": False,
        })

    return args
