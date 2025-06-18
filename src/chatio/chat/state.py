
from collections.abc import Callable

from dataclasses import dataclass

from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.params import ApiParams

from chatio.core import ApiHelper


@dataclass
class ChatState[
    SystemContent,
    MessageContent,
    PredictionContent,
    TextMessage,
    ImageMessage,
    ToolDefinition,
    ToolDefinitions,
    ToolSelection,
]:

    system: SystemContent | None
    messages: list[MessageContent]
    prediction: PredictionContent | None
    tools: ToolDefinitions | None
    funcs: dict[str, Callable]
    tool_choice: ToolSelection | None

    def __init__(
            self,
            api: ApiHelper[
                SystemContent,
                MessageContent,
                PredictionContent,
                TextMessage,
                ImageMessage,
                ToolDefinition,
                ToolDefinitions,
                ToolSelection,
            ],
            state: StateConfig | None = None,
            tools: ToolsConfig | None = None):

        self._api = api

        self.system = None
        self.messages = []
        self.prediction = None
        self.tools = None
        self.funcs = {}
        self.tool_choice = None

        self.update_system_message(state.system if state is not None else None)

        self.setup_message_history(state.messages if state is not None else None)

        self.setup_tool_definitions(tools)

    # messages

    def commit_input_message(self, message: str) -> None:
        self.messages.append(self._api.format.input_message(message))

    def commit_output_message(self, message: str) -> None:
        self.messages.append(self._api.format.input_message(message))

    def commit_call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> None:
        self.messages.append(self._api.format.call_request(tool_call_id, tool_name, tool_input))

    def commit_call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> None:
        self.messages.append(self._api.format.call_response(tool_call_id, tool_name, tool_output))

    def attach_image_document(self, blob: bytes, mimetype: str) -> None:
        self.messages.append(self._api.format.image_document(blob, mimetype))

    def update_system_message(self, message: str | None) -> None:
        if not message:
            self.system = None
            return

        self.system = self._api.format.system_content(self._api.format.text_chunk(message))

    def setup_message_history(self, messages: list[str] | None) -> None:
        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            if not index % 2:
                self.commit_input_message(message)
            else:
                self.commit_output_message(message)

    def touch_message_history(self):
        self.messages = self._api.format.chat_messages(self.messages)

    def use_prediction_content(self, message: str | None) -> None:
        if message is None:
            self.prediction = None
            return

        self.prediction = self._api.format.prediction_content(self._api.format.text_chunk(message))

    # functions

    def setup_tool_definitions(self, tools: ToolsConfig | None) -> None:
        if tools is None:
            tools = ToolsConfig()

        _tool_definitions = []
        self.funcs = {}

        if tools.tools is None:
            tools.tools = {}

        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            _tool_definitions.append(self._api.format.tool_definition(name, desc, schema))

            self.funcs[name] = tool

        self.tools = self._api.format.tool_definitions(_tool_definitions)

        self.tool_choice = self.setup_tool_selection(tools)

    def setup_tool_selection(self, tools: ToolsConfig):
        if not tools.tool_choice_mode and not tools.tool_choice_name:
            return None

        if not tools.tools:
            raise ValueError

        if not tools.tool_choice_name:
            match tools.tool_choice_mode:
                case 'none':
                    return self._api.format.tool_selection_none()
                case 'auto':
                    return self._api.format.tool_selection_auto()
                case 'any':
                    return self._api.format.tool_selection_any()
                case _:
                    raise ValueError
        else:
            if tools.tool_choice_name not in tools.tools:
                raise ValueError

            match tools.tool_choice_mode:
                case 'name':
                    return self._api.format.tool_selection_name(tools.tool_choice_name)
                case _:
                    raise ValueError

    def __call__(self) -> ApiParams:
        return ApiParams(
            system=self.system,
            messages=self.messages,
            prediction=self.prediction,
            tools=self.tools,
            tool_choice=self.tool_choice,
        )
