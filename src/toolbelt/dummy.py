
from collections.abc import Mapping

from . import ToolBase


class DummyTool(ToolBase):

    __desc__: str = (
        "Tool that does nothing and returns nothing. Do not use it please. "
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
    )

    __schema__: Mapping = {
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
