
from dataclasses import dataclass

from typing import override


from google.genai.types import ContentDict
from google.genai.types import ContentUnionDict
from google.genai.types import PartDict

from google.genai.types import ToolConfigDict
from google.genai.types import ToolListUnionDict
from google.genai.types import FunctionDeclarationDict

from chatio.core.params import ApiParamsBuilder
from chatio.core.params import ApiParams


@dataclass
class GoogleParams(ApiParams[
    ContentDict,
    ContentUnionDict,
    None,
    ToolListUnionDict,
    ToolConfigDict,
]):
    pass


class GoogleParamsBuilder(ApiParamsBuilder[
    ContentDict,
    ContentUnionDict,
    None,
    PartDict,
    PartDict,
    PartDict,
    FunctionDeclarationDict,
    ToolListUnionDict,
    ToolConfigDict,
]):

    @override
    def spawn(self) -> GoogleParams:
        return GoogleParams()

    @override
    def build(self) -> GoogleParams:
        params = self.spawn()
        self.setup(params)
        return params
