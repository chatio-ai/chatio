
from . import ToolBase


class ImageDumpTool(ToolBase):
    
    __desc__ = "Dump summary of image analysis. Summary should include key colors (r,g,b) and image description."

    __schema__ = {
        "type": "object",
        "properties": {
            "info": {
                "type": "object",
                "description": "image summary wrapping structure",
                "properties": {
                    "r": {
                        "type": "number",
                        "description": "red value [0.0, 1.0]",
                    },
                    "g": {
                        "type": "number",
                        "description": "green value [0.0, 1.0]",
                    },
                    "b": {
                        "type": "number",
                        "description": "blue value [0.0, 1.0]",
                    },
                    "desc": {
                        "type": "string",
                        "description": "image description",
                    },
                },
                "required": ["r", "g", "b"],
            },
        },
        "required": ["info"],
    }

    def __call__(self, info=None):
        return
        yield
