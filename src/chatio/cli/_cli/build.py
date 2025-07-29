
import asyncio

from chatio.chat import Chat
from chatio.misc import build_chat as _build_chat


async def build_chat(
    prompt: str | None = None,
    messages: list[str] | None = None,
    tools: str | None = None,
    model: str | None = None,
) -> Chat:
    return await asyncio.to_thread(lambda: _build_chat(
        prompt=prompt,
        messages=messages,
        tools=tools,
        model=model,
    ))
