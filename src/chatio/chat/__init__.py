
from collections.abc import Iterator

from dataclasses import dataclass

from chatio.core.config import ModelConfig
from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.client import ApiClient

from chatio.core.events import CallEvent, DoneEvent, StatEvent, TextEvent


from .state import build_state
from .state import ChatState

from .tools import build_tools
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
        client: ApiClient,
        model: ModelConfig,
        state: StateConfig | None = None,
        tools: ToolsConfig | None = None,
    ) -> None:

        self._client = client

        self._model = model

        self._state = build_state(state)

        self._tools = build_tools(tools)

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

        self._state.commit_call_response(tool_call_id, tool_name, content)

    def __call__(self, content: str | None = None) -> Iterator[dict]:
        if content:
            self._state.commit_input_message(content)

        return self._iterate()

    def _iterate(self) -> Iterator[dict]:
        calls = -1
        while calls:
            calls = 0

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
                            self._state.commit_output_message(text)
                    case CallEvent(call_id, name, args, args_raw):
                        self._state.commit_call_request(call_id, name, args_raw)
                        yield {
                            "type": "tools_usage",
                            "tool_name": name,
                            "tool_args": args,
                        }
                        yield from self._process_tool_call(call_id, name, args)
                        calls += 1
                    case StatEvent():
                        yield from self._usage(event)

    # helpers

    def count_tokens(self, content: str | None = None) -> int:
        if content:
            self._state.commit_input_message(content)

        return self._client.count_message_tokens(self._model.model, self._state, self._tools)

    def info(self) -> ChatInfo:
        return ChatInfo(
            self._model.vendor,
            self._model.model,
            len(self._tools.funcs),
            bool(self._state.system),
            len(self._state.messages),
        )
