
from dataclasses import dataclass

from typing import override

from chatio.core.object import Closeable

from chatio.core.config import ModelConfig


from .model import init_client
from .state import ChatState
from .tools import ChatTools
from .reply import ChatReply


@dataclass
class ChatInfo:
    vendor: str
    model: str
    tools: int
    system: int
    messages: int


class Chat(Closeable):

    def __init__(
        self,
        model: ModelConfig,
        state: ChatState | None = None,
        tools: ChatTools | None = None,
    ) -> None:

        self._model = model

        self._client = init_client(model.config)

        if state is None:
            state = ChatState()
        self._state = state

        if tools is None:
            tools = ChatTools()
        self._tools = tools

    @property
    def state(self) -> ChatState:
        return self._state

    @property
    def tools(self) -> ChatTools:
        return self._tools

    @override
    async def close(self) -> None:
        await self._client.close()

    # streams

    def stream_content(self) -> ChatReply:
        model = self._model.model
        return ChatReply(
            lambda state, tools: self._client.iterate_model_events(model, state, tools),
            self._state, self._tools)

    # helpers

    async def count_tokens(self) -> int:
        return await self._client.count_message_tokens(self._model.model, self._state, self._tools)

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._model.vendor,
            self._model.model,
            len(self._tools.tools),
            bool(self._state.options.system),
            len(self._state.messages),
        )
