
from collections.abc import Callable

from dataclasses import dataclass, field

from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig


@dataclass
class ContentEntry:
    pass


@dataclass
class CallRequest(ContentEntry):
    tool_call_id: str
    tool_name: str
    tool_input: object


@dataclass
class CallResponse(ContentEntry):
    tool_call_id: str
    tool_name: str
    tool_output: str


@dataclass
class TextMessage(ContentEntry):
    text: str


@dataclass
class SystemMessage(TextMessage):
    pass


@dataclass
class InputMessage(TextMessage):
    pass


@dataclass
class OutputMessage(TextMessage):
    pass


@dataclass
class PredictMessage(TextMessage):
    pass


@dataclass
class ImageDocument(ContentEntry):
    blob: bytes
    mimetype: str


@dataclass
class TextDocument(ContentEntry):
    text: str
    mimetype: str


@dataclass
class ToolConfig:
    name: str
    desc: str
    schema: dict


@dataclass
class ToolChoice:
    mode: str | None
    name: str | None
    tools: list[str]


@dataclass
class ChatState:
    system: SystemMessage | None = None
    messages: list[ContentEntry] = field(default_factory=list)
    extras: dict[str, ContentEntry | None] = field(default_factory=dict)

    def __init__(self, state: StateConfig | None = None) -> None:
        super().__init__()

        if state is None:
            state = StateConfig()

        if state.system is not None:
            self.system = SystemMessage(state.system)

        if state.messages is None:
            state.messages = []

        for index, message in enumerate(state.messages):
            if not index % 2:
                self.messages.append(InputMessage(message))
            else:
                self.messages.append(OutputMessage(message))


@dataclass
class ChatTools:
    funcs: dict[str, Callable] = field(default_factory=dict)
    tools: list[ToolConfig] | None = None
    tool_choice: ToolChoice | None = None

    def __init__(self, tools: ToolsConfig | None = None) -> None:
        super().__init__()

        if tools is None:
            tools = ToolsConfig()

        if tools.tools is None:
            return

        self.tools = []
        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            self.funcs[name] = tool

            self.tools.append(ToolConfig(name, desc, schema))

        self.tool_choice = \
            ToolChoice(tools.tool_choice_mode, tools.tool_choice_name, list(tools.tools))
