
import asyncio

from chatio.misc.model import build_model
from chatio.misc.state import build_state
from chatio.misc.tools import build_tools
from chatio.chat import Chat


async def build_chat(
    prompt: str | None = None,
    messages: list[str] | None = None,
    tools: str | None = None,
    model: str | None = None,
) -> Chat:
    return await asyncio.to_thread(lambda: Chat(
        model=build_model(model),
        state=build_state(prompt, messages),
        tools=build_tools(tools),
    ))
