
from chatio.core.config import StateConfig

from chatio.core.models import SystemMessage
from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ChatState


def build_state(state: StateConfig | None = None) -> ChatState:
    _state = ChatState()

    if state is None:
        state = StateConfig()

    if state.system is not None:
        _state.system = SystemMessage(state.system)

    if state.messages is None:
        state.messages = []

    for index, message in enumerate(state.messages):
        if not index % 2:
            _state.messages.append(InputMessage(message))
        else:
            _state.messages.append(OutputMessage(message))

    return _state
