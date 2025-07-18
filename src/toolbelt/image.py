
from collections.abc import Iterator

from typing import override

from . import ToolSchemaDict
from . import ToolBase


class ImageDumpTool(ToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "image_dump",
            "description": "Dump image analysis result. Summary includes key colors (r,g,b) and description.",
            "type": "object",
            "properties": {
                "info": {
                    "type": "object",
                    "description": "Structure to wrap all the details of image summary.",
                    "properties": {
                        "r": {
                            "type": "number",
                            "description": "red value component [0.0, 1.0].",
                        },
                        "g": {
                            "type": "number",
                            "description": "green value component [0.0, 1.0].",
                        },
                        "b": {
                            "type": "number",
                            "description": "blue value component [0.0, 1.0].",
                        },
                        "desc": {
                            "type": "string",
                            "description": "Text description of the image.",
                        },
                    },
                    "required": ["r", "g", "b"],
                },
            },
            "required": ["info"],
        }

    @override
    def __call__(self, info=None) -> Iterator[str]:
        return
        yield info
