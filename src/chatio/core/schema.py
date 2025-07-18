
from __future__ import annotations

from typing import TypedDict


class ToolParamDict(TypedDict, total=False):
    type: str

    description: str

    properties: dict[str, ToolParamDict] | None

    required: list[str] | None


class ToolSchemaDict(ToolParamDict, total=False):
    name: str
