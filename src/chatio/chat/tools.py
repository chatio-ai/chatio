
from dataclasses import dataclass

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


type Func = Callable[..., AsyncIterator[str | dict[str, object]]]


@dataclass
class ChatTools(_ChatTools):
    def __init__(
        self,
        tools: list[ToolBase] | None = None,
        tool_choice_mode: str | None = None,
        tool_choice_name: str | None = None,
    ) -> None:
        self._functions: dict[str, Func] = {}

        if tools is None:
            tools = []

        schemas = []
        for tool in tools:
            schema = tool.schema()
            name = schema.pop("name")
            desc = schema.pop("description")

            if not name or not desc or not schema:
                raise RuntimeError

            self._functions[name] = tool.__call__
            schemas.append(ToolSchema(name, desc, schema))

        if tool_choice_name and tool_choice_name not in self._functions:
            raise ValueError
        choice = ToolChoice(tool_choice_mode, tool_choice_name)

        super().__init__(schemas, choice)

    async def _do_call(self, call: CallEvent, state: ChatState) -> AsyncIterator[ChatEvent]:
        function = self._functions.get(call.name)
        if not function:
            return

        content = ""
        async for event in function(**call.args):
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
            async for event in self._do_call(call, state):
                yield event
