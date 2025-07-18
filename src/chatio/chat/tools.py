
from dataclasses import dataclass, field

from collections.abc import AsyncIterator
from collections.abc import Callable

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.models import ChatTools as _ChatTools

from chatio.core.events import ChatEvent
from chatio.core.events import CallEvent
from chatio.core.events import ToolEvent
from chatio.core.events import ToolsTextChunk

from chatio.core.invoke import ToolBase

from .state import ChatState


@dataclass
class ChatTools(_ChatTools):
    _funcs: dict[str, Callable[..., AsyncIterator[str | dict]]] = field(default_factory=dict)

    def __init__(self, tools: list[ToolBase] | None = None,
                 tool_choice_mode: str | None = None, tool_choice_name: str | None = None) -> None:

        if tools is None:
            tools = []

        _tools = []
        _funcs = {}
        for tool in tools:
            schema = tool.schema()
            name = schema.pop("name")
            desc = schema.pop("description")

            if not name or not desc or not schema:
                raise RuntimeError

            _funcs[name] = tool.__call__
            _tools.append(ToolSchema(name, desc, schema))

        if tool_choice_name and tool_choice_name not in tools:
            raise ValueError
        _tool_choice = ToolChoice(tool_choice_mode, tool_choice_name)

        super().__init__(_tools, _tool_choice)
        self._funcs = _funcs

    async def _call(self, call: CallEvent, state: ChatState) -> AsyncIterator[ChatEvent]:
        tool_func = self._funcs.get(call.name)
        if not tool_func:
            return

        content = ""
        async for event in tool_func(**call.args):
            if isinstance(event, str):
                content += event
                yield ToolsTextChunk(event)
            elif event is not None:
                yield ToolEvent(call.call_id, call.name, event)

        state.append_call_request(call.call_id, call.name, call.args_raw)
        state.append_call_response(call.call_id, call.name, content)

    async def __call__(self, calls: list[CallEvent], state: ChatState) -> AsyncIterator[ChatEvent]:
        for call in calls:
            yield call
            async for event in self._call(call, state):
                yield event
