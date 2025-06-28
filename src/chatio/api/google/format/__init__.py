
from typing import override

from google.genai.types import ContentUnionDict
from google.genai.types import PartDict

from google.genai.types import FunctionDeclarationDict
from google.genai.types import ToolListUnionDict
from google.genai.types import ToolConfigDict


from chatio.core.format import ApiFormat

from chatio.core.models import ChatState
from chatio.core.models import ChatTools

from chatio.api.google.params import GoogleStateOptions
from chatio.api.google.params import GoogleParams
from chatio.api.google.config import GoogleConfig

from .history import GoogleFormatHistory
from .options import GoogleFormatOptions
from .tooling import GoogleFormatTooling


class GoogleFormat(ApiFormat[
    ContentUnionDict,
    PartDict,
    PartDict,
    PartDict,
    ToolListUnionDict,
    FunctionDeclarationDict,
    ToolConfigDict,
    GoogleStateOptions,
    GoogleConfig,
]):

    @property
    @override
    def _format_options(self) -> GoogleFormatOptions:
        return GoogleFormatOptions(self._config)

    @property
    @override
    def _format_history(self) -> GoogleFormatHistory:
        return GoogleFormatHistory(self._config)

    @property
    @override
    def _format_tooling(self) -> GoogleFormatTooling:
        return GoogleFormatTooling(self._config)

    @override
    def build(self, state: ChatState, tools: ChatTools) -> GoogleParams:
        params = self.spawn(state, tools)

        return GoogleParams(
            max_output_tokens=4096,
            system_instruction=params.options.system,
            messages=params.messages,
            tools=params.tools,
            tool_config=params.tool_choice,
        )
