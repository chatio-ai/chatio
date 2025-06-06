
from typing import override

from . import ToolBase


class ImageDumpTool(ToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Dump summary of image analysis. Summary should include key colors (r,g,b) and image description."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
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

    def __call__(self, info=None):
        return
        yield info
