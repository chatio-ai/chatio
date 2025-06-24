
from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.params import ApiParams


class ChatState[ApiParamsT: ApiParams]:

    def __init__(
        self,
        params: ApiParamsT,
        state: StateConfig | None = None,
        tools: ToolsConfig | None = None,
    ):

        self._params = params

        self.update_system_message(state.system if state is not None else None)

        self.setup_message_history(state.messages if state is not None else None)

        self.setup_tool_definitions(tools)

    # messages

    def commit_input_message(self, message: str) -> None:
        self._params.messages.append(self._params.format.input_message(message))

    def commit_output_message(self, message: str) -> None:
        self._params.messages.append(self._params.format.input_message(message))

    def commit_call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> None:
        self._params.messages.append(self._params.format.call_request(tool_call_id, tool_name, tool_input))

    def commit_call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> None:
        self._params.messages.append(self._params.format.call_response(tool_call_id, tool_name, tool_output))

    def attach_image_document(self, blob: bytes, mimetype: str) -> None:
        self._params.messages.append(self._params.format.image_document(blob, mimetype))

    def update_system_message(self, message: str | None) -> None:
        if not message:
            self._params.system = None
            return

        self._params.system = self._params.format.system_content(self._params.format.text_chunk(message))

    def setup_message_history(self, messages: list[str] | None) -> None:
        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            if not index % 2:
                self.commit_input_message(message)
            else:
                self.commit_output_message(message)

    def touch_message_history(self):
        self._params.messages = self._params.format.chat_messages(self._params.messages)

    def use_prediction_content(self, message: str | None) -> None:
        if message is None:
            self._params.prediction = None
            return

        self._params.prediction = self._params.format.prediction_content(self._params.format.text_chunk(message))

    # functions

    def setup_tool_definitions(self, tools: ToolsConfig | None) -> None:
        if tools is None:
            tools = ToolsConfig()

        _tool_definitions = []

        if tools.tools is None:
            tools.tools = {}

        for name, tool in tools.tools.items():
            desc = tool.desc()
            schema = tool.schema()

            if not name or not desc or not schema:
                raise RuntimeError

            _tool_definitions.append(self._params.format.tool_definition(name, desc, schema))

            self._params.funcs[name] = tool

        self._params.tools = self._params.format.tool_definitions(_tool_definitions)

        self._params.tool_choice = self.setup_tool_selection(tools)

    def setup_tool_selection(self, tools: ToolsConfig):
        if not tools.tool_choice_mode and not tools.tool_choice_name:
            return None

        if not tools.tools:
            raise ValueError

        if not tools.tool_choice_name:
            match tools.tool_choice_mode:
                case 'none':
                    return self._params.format.tool_selection_none()
                case 'auto':
                    return self._params.format.tool_selection_auto()
                case 'any':
                    return self._params.format.tool_selection_any()
                case _:
                    raise ValueError
        else:
            if tools.tool_choice_name not in tools.tools:
                raise ValueError

            match tools.tool_choice_mode:
                case 'name':
                    return self._params.format.tool_selection_name(tools.tool_choice_name)
                case _:
                    raise ValueError

    def __call__(self) -> ApiParamsT:
        return self._params
