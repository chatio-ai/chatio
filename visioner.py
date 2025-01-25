#!/usr/bin/env python

import sys

import dotenv

from textwrap import dedent

from chatutil.api import Chat, do_image
from chatutil.ui import run_chat



def run_imgdump(info=None):
    from pprint import pprint
    pprint(info)

run_imgdump_desc = {
    "name": "run_imgdump",
    "description": "Dump summary of image analysis. Summary should include key colors (r,g,b) and image description.",
    "input_schema": {
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
    },
    "func": run_imgdump,
}

dotenv.load_dotenv()

chat = Chat(tools=[run_imgdump_desc], tool_choice='name', tool_choice_name='run_imgdump')


if __name__ == '__main__':

    content = []

    for filename in sys.argv[1:]:
        content.extend(do_image(filename))

    if not content:
        raise SystemExit()

    run_chat(chat, content)

    print()
