

import os

import httpx


def log_request(request: httpx.Request) -> None:
    content = request.content.decode()
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    print(f"{request.method} {request.url}\n{headers}\n\n{content}\n\n")


def log_response(response: httpx.Response) -> None:
    headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
    print(f"{response.http_version} {response.status_code}\n{headers}\n\n")


def httpx_args() -> dict:
    if not os.getenv("CHATIO_HTTPX_DEBUG"):
        return {}

    return {
        "event_hooks": {
            "request": [log_request],
            "response": [log_response],
        },
    }
