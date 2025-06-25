
from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.models import PredictMessage
from chatio.core.models import SystemMessage
from chatio.core.models import OutputMessage
from chatio.core.models import InputMessage

from chatio.core.models import ImageDocument
from chatio.core.models import CallResponse
from chatio.core.models import CallRequest

from chatio.core.models import ToolSchema
from chatio.core.models import ToolChoice

from chatio.core.params import ApiParams


class ChatState:

    def __init__(
            self,
            state: StateConfig | None = None,
            tools: ToolsConfig | None = None):

        self._params = ApiParams()

        self.update_system_message(state.system if state is not None else None)

        self.setup_message_history(state.messages if state is not None else None)

        self.setup_tool_definitions(tools)

    # messages

    def commit_input_message(self, message: str) -> None:
        self._params.messages.append(InputMessage(message))

    def commit_output_message(self, message: str) -> None:
        self._params.messages.append(OutputMessage(message))

    def commit_call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> None:
        self._params.messages.append(CallRequest(tool_call_id, tool_name, tool_input))

    def commit_call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> None:
        self._params.messages.append(CallResponse(tool_call_id, tool_name, tool_output))

    def attach_image_document(self, blob: bytes, mimetype: str) -> None:
        self._params.messages.append(ImageDocument(blob, mimetype))

    def update_system_message(self, message: str | None) -> None:
        self._params.system = None
        if message is not None:
            self._params.system = SystemMessage(message)

    def setup_message_history(self, messages: list[str] | None) -> None:
        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            if not index % 2:
                self.commit_input_message(message)
            else:
                self.commit_output_message(message)

    def use_prediction_content(self, message: str | None) -> None:
        self._params.predict = None
        if message is not None:
            self._params.predict = PredictMessage(message)

    # functions

    def setup_tool_definitions(self, tools: ToolsConfig | None) -> None:
        if tools is None:
            return

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
