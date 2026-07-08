
from chatio.chat import Chat

from chatio.chat.state import ChatState


from .model import build_model
from .tools import build_tools


def build_chat(
    prompt: str | None = None,
    messages: list[str] | None = None,
    tools: str | None = None,
    model: str | None = None,
) -> Chat:
    return Chat(
        model=build_model(model),
        state=build_state(prompt, messages),
        tools=build_tools(tools),
    )


def build_state(prompt: str | None = None, messages: list[str] | None = None) -> ChatState:
    return ChatState(prompt, messages)
