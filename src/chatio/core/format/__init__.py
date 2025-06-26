
from abc import ABC, abstractmethod

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.core.params import ApiParams

from .state import ApiFormatState
from .tools import ApiFormatTools


class ApiFormat[
    SystemContentT,
    MessageContentT,
    ChatPredictionT,
    TextMessageT,
    ImageDocumentT,
    TextDocumentT,
    ToolDefinitionT,
    ToolDefinitionsT,
    ToolSelectionT,
](ABC):

    def setup(self, params: ApiParams[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ], state: ChatState, tools: ChatTools):
        # _predict = state.extras.get('prediction')
        # if _predict is not None and not isinstance(_predict, PredictMessage):
        #     raise TypeError(_predict)

        params.system = self._format_state.system(state.system)
        params.messages = self._format_state.messages(state.messages)
        # params.predict = self._format_state.predict(_predict)
        params.tools = self._format_tools.tools(tools.tools)
        params.tool_choice = self._format_tools.tool_choice(tools.tool_choice)

    @property
    @abstractmethod
    def _format_state(self) -> ApiFormatState[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        TextMessageT,
        ImageDocumentT,
        TextDocumentT,
    ]:
        ...

    @property
    @abstractmethod
    def _format_tools(self) -> ApiFormatTools[
        ToolDefinitionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ]:
        ...

    @abstractmethod
    def build(self, state: ChatState, tools: ChatTools) -> ApiParams[
        SystemContentT,
        MessageContentT,
        ChatPredictionT,
        ToolDefinitionsT,
        ToolSelectionT,
    ]:
        ...
