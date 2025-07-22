
import os

from collections.abc import AsyncIterator

from typing import override

import httpx


class LoggingResponse(httpx.Response):

    @override
    async def aiter_bytes(self, chunk_size: int | None = None) -> AsyncIterator[bytes]:
        buffer = bytearray()
        async for chunk in super().aiter_bytes(chunk_size):
            print(chunk.decode())
            buffer.extend(chunk)
            yield b""
        yield bytes(buffer)


class LoggingTransport(httpx.AsyncHTTPTransport):

    def __init__(self, *, verbose: bool = False) -> None:
        super().__init__()
        self.verbose = verbose

    async def _log_request(self, request: httpx.Request) -> None:
        content = request.content.decode()
        headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
        print(f"{request.method} {request.url}\n{headers}\n\n{content}\n\n")

    async def _log_response(self, response: httpx.Response) -> None:
        headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
        print(f"{response.http_version} {response.status_code}\n{headers}\n\n")

    @override
    async def handle_async_request(self,
                                   request: httpx.Request, **kwargs: object) -> httpx.Response:

        await self._log_request(request)
        response = await super().handle_async_request(request, **kwargs)
        await self._log_response(response)

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
