
from collections.abc import Iterator

from dataclasses import dataclass

from chatio.core.config import ModelConfig

from chatio.core.events import CallEvent, DoneEvent, StatEvent, TextEvent


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

    def _process_tool_call(self, tool_call_id: str, tool_name: str, tool_args: dict) -> Iterator[dict]:
        tool_func = self._tools.funcs.get(tool_name)
        if not tool_func:
            return

        content = ""
        for chunk in tool_func(**tool_args):
            if isinstance(chunk, str):
                content += chunk
                yield {
                    "type": "tools_chunk",
                    "text": chunk,
                }
            elif chunk is not None:
                yield {
                    "type": "tools_event",
                    "tool_name": tool_name,
                    "tool_data": chunk,
                }

        self._state.append_call_response(tool_call_id, tool_name, content)

    def __call__(self, content: str | None = None) -> Iterator[dict]:
        if content:
            self._state.append_input_message(content)

        return self._iterate()

    def _iterate(self) -> Iterator[dict]:
        calls: list[CallEvent] = []
        stats: list[StatEvent] = []

        events = None
        while not events or calls:
            calls.clear()
            stats.clear()

            events = self._client.iterate_model_events(self._model.model, self._state, self._tools)

            for event in events:
                match event:
                    case TextEvent(text, label):
                        yield {
                            "type": "model_chunk",
                            "label": label,
                            "text": text,
                        }
                    case DoneEvent(text):
                        if text:
                            self._state.append_output_message(text)
                    case CallEvent():
                        calls.append(event)
                    case StatEvent():
                        stats.append(event)

            yield from self._usage(stats)

            for call in calls:
                self._state.append_call_request(call.call_id, call.name, call.args_raw)
                yield {
                    "type": "tools_usage",
                    "tool_name": call.name,
                    "tool_args": call.args,
                }
                yield from self._process_tool_call(call.call_id, call.name, call.args)

    # helpers

    def count_tokens(self, content: str | None = None) -> int:
        if content:
            self._state.append_input_message(content)

        return self._client.count_message_tokens(self._model.model, self._state, self._tools)

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._model.vendor,
            self._model.model,
            len(self._tools.funcs),
            bool(self._state.options.system),
            len(self._state.messages),
        )
