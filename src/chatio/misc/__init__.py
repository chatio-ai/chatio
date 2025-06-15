
import os
import json
import logging

from pathlib import Path

from chatio.core.config import ApiConfig
from chatio.core.config import ChatConfig
from chatio.core.config import ToolConfig

from chatio.core.format import ToolChoice

from chatio.api.claude import ClaudeApi
from chatio.api.google import GoogleApi
from chatio.api.openai import OpenAIApi

from chatio.chat import ChatBase

from toolbelt.shell import ShellCalcTool, ShellExecTool
from toolbelt.dummy import DummyTool

from toolbelt.wiki import WikiToolFactory
from toolbelt.web import WebSearchTool, WebBrowseTool

from toolbelt.image import ImageDumpTool

from toolbelt.llm import LlmDialogTool


def setup_logging() -> None:
    logging.basicConfig(filename='chunkapi.log', filemode='a', level=100,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')
    logging.getLogger('chatio.api').setLevel(logging.INFO)


def init_config(model_name: str | None = None, env_name: str | None = None) -> ChatConfig:
    if model_name is not None and env_name is not None:
        raise ValueError

    if model_name is None:
        if env_name is None:
            env_name = 'CHATIO_MODEL_NAME'

        model_name = os.environ.get(env_name)
        if not model_name or '/' not in model_name:
            err_msg = f"Configure {env_name}!"
            raise RuntimeError(err_msg)

    vendor_name, _, model_name = model_name.partition('/')
    vendor_conf = Path("./vendors").joinpath(vendor_name + ".json")

    with vendor_conf.open() as vendorfp:
        vendor_json = json.load(vendorfp)

    vendor_json = {k: v for k, v in vendor_json.items() if not k.startswith('_')}

    return ChatConfig(vendor_name, model_name, ApiConfig(**vendor_json))


def build_chat(
        system: str | None = None,
        messages: list[str] | None = None,
        tools: ToolConfig | None = None,
        config: ChatConfig | None = None) -> ChatBase:

    if config is None:
        err_msg = "no config specified!"
        raise RuntimeError
    if config.model is None:
        err_msg = "no model specified!"
        raise RuntimeError(err_msg)

    match config.config.api_cls:
        case 'claude':
            return ChatBase(ClaudeApi(config), system, messages, tools)
        case 'google':
            return ChatBase(GoogleApi(config), system, messages, tools)
        case 'openai':
            return ChatBase(OpenAIApi(config), system, messages, tools)
        case _:
            err_msg = f"api_cls not supported: {config.config.api_cls}"
            raise RuntimeError(err_msg)


def default_tools(tools_name: str | None = None, env_name: str | None = None) -> ToolConfig:
    if tools_name is not None and env_name is not None:
        raise ValueError

    if tools_name is None:
        if env_name is None:
            env_name = 'CHATIO_TOOLS_NAME'

        tools_name = os.environ.get(env_name)
        if not tools_name:
            tools_name = 'empty'

    match tools_name:
        case 'default':
            wiki = WikiToolFactory()

            return ToolConfig({
                "run_command": ShellExecTool(),
                "run_bc_calc": ShellCalcTool(),
                "wiki_content": wiki.wiki_content(),
                "wiki_summary": wiki.wiki_summary(),
                "wiki_section": wiki.wiki_section(),
                "wiki_search": wiki.wiki_search(),
                "web_search": WebSearchTool(),
                "web_browse": WebBrowseTool(),
                "run_nothing": DummyTool(),
            })
        case 'llmtool':
            llm = build_chat(
                config=init_config(env_name='CHATIO_NESTED_MODEL_NAME'),
                tools=default_tools(env_name='CHATIO_NESTED_TOOLS_NAME'))

            return ToolConfig({
                "llm_message": LlmDialogTool(llm),
            })
        case 'imgtool':
            return ToolConfig({
                "run_imgdump": ImageDumpTool(),
            }, tool_choice=ToolChoice.NAME, tool_choice_name='run_imgdump')
        case _:
            return ToolConfig()
