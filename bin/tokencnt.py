#!/usr/bin/env python

import sys

import dotenv

from chatio.api import build_chat
from chatio.misc import init_config

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.image import ImageDumpTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory


dotenv.load_dotenv()

if __name__ == '__main__':
    prompt = " ".join(sys.argv[1:])
    content = sys.stdin.read()
    if not content.strip():
        raise SystemExit()

    wiki = WikiToolFactory()
    chat = build_chat(prompt, messages=[content], tools={
        "run_command": ShellExecTool(),
        "run_bc_calc": ShellCalcTool(),
        "run_imgdump": ImageDumpTool(),
        "wiki_content": wiki.wiki_content(),
        "wiki_summary": wiki.wiki_summary(),
        "wiki_section": wiki.wiki_section(),
        "wiki_search": wiki.wiki_search(),
        "run_nothing": DummyTool(),
    }, config=init_config())

    print(chat._token_count())
