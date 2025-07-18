
from collections.abc import Iterator

from dataclasses import dataclass

from chatio.core.config import ModelConfig

from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import ToolEvent
from chatio.core.events import StopEvent
from chatio.core.events import StatEvent
from chatio.core.events import ModelTextChunk
from chatio.core.events import ToolsTextChunk


from .model import init_client
from .state import ChatState
from .tools import ChatTools
from .usage import ChatUsage


@dataclass
class ChatInfo:
    vendor: str
    model: str
    tools: int
    system: int
    messages: int


class Chat:

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

        self._usage = ChatUsage()

    @property
    def state(self) -> ChatState:
        return self._state

    @property
    def tools(self) -> ChatTools:
        return self._tools

    # streams

    def _process_tool_call(self, call: CallEvent) -> Iterator[ChatEvent]:
        tool_func = self._tools.funcs.get(call.name)
        if not tool_func:
            return

        content = ""
        for event in tool_func(**call.args):
            if isinstance(event, str):
                content += event
                yield ToolsTextChunk(event)
            elif event is not None:
                yield ToolEvent(call.call_id, call.name, event)

        self._state.append_call_response(call.call_id, call.name, content)

    def stream_content(self) -> Iterator[ChatEvent]:
        calls: list[CallEvent] = []
        stats: list[StatEvent] = []

        events = None
        while not events or calls:
            calls.clear()
            stats.clear()

            events = self._client.iterate_model_events(self._model.model, self._state, self._tools)

            for event in events:
                match event:
                    case ModelTextChunk():
                        yield event
                    case StopEvent(text):
                        if text:
                            self._state.append_output_message(text)
                    case CallEvent():
                        calls.append(event)
                    case StatEvent():
                        stats.append(event)

            yield from self._usage(stats)

            for call in calls:
                self._state.append_call_request(call.call_id, call.name, call.args_raw)
                yield call
                yield from self._process_tool_call(call)

    # helpers

    def count_tokens(self) -> int:
        return self._client.count_message_tokens(self._model.model, self._state, self._tools)

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._model.vendor,
            self._model.model,
            len(self._tools.funcs),
            bool(self._state.options.system),
            len(self._state.messages),
        )
