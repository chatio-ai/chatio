
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
class ToolSchema:
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

    @classmethod
    def build(cls, state: StateConfig | None = None) -> 'ChatState':
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


@dataclass
class ChatTools:
    funcs: dict[str, Callable] = field(default_factory=dict)
    tools: list[ToolSchema] | None = None
    tool_choice: ToolChoice | None = None

    @classmethod
    def build(cls, tools: ToolsConfig | None = None) -> 'ChatTools':
        _tools = ChatTools()

        if tools is None:
            return _tools

        if tools.tools is None:
            tools.tools = {}

        _tools.tools = []
        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            _tools.funcs[name] = tool

            _tools.tools.append(ToolSchema(name, desc, schema))

        _tools.tool_choice = ToolChoice(
            tools.tool_choice_mode, tools.tool_choice_name, list(tools.tools))

        return _tools
