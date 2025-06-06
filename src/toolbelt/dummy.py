
from typing import override

from . import ToolBase


class DummyTool(ToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return (
            "Tool that does nothing and returns nothing. Do not use it please. "
            "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
            "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
            "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
            "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
        )

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "dummy": {
                    "type": "string",
                    "description": "dummy value",
                },
            },
        }

    def __call__(self, dummy=None):
        return
        yield dummy
