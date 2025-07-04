
from dataclasses import dataclass

from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.models import SystemMessage
from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.params import ApiParams


@dataclass
class ChatState:

    def __init__(self, state: StateConfig | None = None, tools: ToolsConfig | None = None) -> None:

        self._params = ApiParams()

        if state is None:
            state = StateConfig()

        self._init_state(state)

        if tools is None:
            tools = ToolsConfig()

        self._init_tools(tools)

    def _init_state(self, state: StateConfig) -> None:
        if state.system is not None:
            self._params.system = SystemMessage(state.system)

        if state.messages is None:
            state.messages = []

        for index, message in enumerate(state.messages):
            if not index % 2:
                self._params.messages.append(InputMessage(message))
            else:
                self._params.messages.append(OutputMessage(message))

    def _init_tools(self, tools: ToolsConfig) -> None:
        self._params.tools = []

        if tools.tools is None:
            tools.tools = {}

        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            self._params.funcs[name] = tool

            self._params.tools.append(ToolSchema(name, desc, schema))

        self._params.tool_choice = \
            ToolChoice(tools.tool_choice_mode, tools.tool_choice_name, list(tools.tools))

    def __call__(self) -> ApiParams:
        return self._params
