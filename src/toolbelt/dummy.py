
from collections.abc import Iterator

from typing import override

from . import ToolSchemaDict
from . import ToolBase


class DoNothingTool(ToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "do_nothing",
            "description": (
                "Tool that does nothing and returns nothing. Do not use it please. "
                "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
                "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
                "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
                "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
            ),
            "type": "object",
            "properties": {
                "dummy": {
                    "type": "string",
                    "description": "dummy value",
                },
            },
        }

    @override
    def __call__(self, dummy=None) -> Iterator[str]:
        return
        yield dummy
