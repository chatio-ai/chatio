
import os

import httpx


def _log_request(request: httpx.Request) -> None:
    content = request.content.decode()
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    print(f"{request.method} {request.url}\n{headers}\n\n{content}\n\n")


def _log_response(response: httpx.Response) -> None:
    headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
    print(f"{response.http_version} {response.status_code}\n{headers}\n\n")


def httpx_args() -> dict:
    args: dict[str, object] = {}

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
