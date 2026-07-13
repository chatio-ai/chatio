
from chatio.chat.state import ChatState


def build_state(prompt: str | None = None, messages: list[str] | None = None) -> ChatState:
    return ChatState(prompt, messages)
