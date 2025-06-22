
import os
import json
import logging

from pathlib import Path

from chatio.core.config import ModelConfig
from chatio.core.config import StateConfig
from chatio.core.config import ToolsConfig

from chatio.core.params import ApiParams

from chatio.api.custom import CustomApi

from chatio.api.claude.config import ClaudeConfigOptions
from chatio.api.claude.config import ClaudeConfig
from chatio.api.claude.params import ClaudeParams
from chatio.api.claude import ClaudeApi

from chatio.api.google.config import GoogleConfigOptions
from chatio.api.google.config import GoogleConfig
from chatio.api.google.params import GoogleParams
from chatio.api.google import GoogleApi

from chatio.api.openai.config import OpenAIConfigOptions
from chatio.api.openai.config import OpenAIConfig
from chatio.api.openai.params import OpenAIParams
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


def init_model(model_name: str | None = None, env_name: str | None = None) -> ModelConfig:
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

    return ModelConfig(vendor_name, model_name)


def vendor_json(vendor_name: str) -> dict:
    vendor_file = Path("./vendors").joinpath(vendor_name + ".json")

    with vendor_file.open() as vendorfp:
        vendor_data = json.load(vendorfp)

    return {k: v for k, v in vendor_data.items() if not k.startswith('_')}


def parse_opts(api_options: str | None = None, env_name: str | None = None) -> dict:
    if api_options is not None and env_name is not None:
        raise ValueError

    if api_options is None:
        if env_name is None:
            env_name = 'CHATIO_API_OPTIONS'

        api_options = os.environ.get(env_name)
        if not api_options:
            return {}

    return json.loads(api_options)


def build_chat_claude(
    config_data: dict,
    options_data: dict,
    model: ModelConfig,
    state: StateConfig | None = None,
    tools: ToolsConfig | None = None,
) -> ChatBase[ClaudeParams]:
    options = ClaudeConfigOptions(**options_data)
    config = ClaudeConfig(**config_data, options=options)
    return ChatBase(ClaudeApi(config), model, state, tools)


def build_chat_google(
    config_data: dict,
    options_data: dict,
    model: ModelConfig,
    state: StateConfig | None = None,
    tools: ToolsConfig | None = None,
) -> ChatBase[GoogleParams]:
    options = GoogleConfigOptions(**options_data)
    config = GoogleConfig(**config_data, options=options)
    return ChatBase(GoogleApi(config), model, state, tools)


def build_chat_openai(
    config_data: dict,
    options_data: dict,
    model: ModelConfig,
    state: StateConfig | None = None,
    tools: ToolsConfig | None = None,
) -> ChatBase[OpenAIParams]:
    options = OpenAIConfigOptions(**options_data)
    config = OpenAIConfig(**config_data, options=options)
    return ChatBase(OpenAIApi(config), model, state, tools)


def build_chat_custom(
    config_data: dict,
    options_data: dict,
    model: ModelConfig,
    state: StateConfig | None = None,
    tools: ToolsConfig | None = None,
) -> ChatBase[ApiParams]:

    claude_options = ClaudeConfigOptions(**options_data)
    claude_config = ClaudeConfig(**config_data, options=claude_options)

    openai_options = OpenAIConfigOptions(**options_data)
    openai_config = OpenAIConfig(**config_data, options=openai_options)

    helper = CustomApi(claude_config, openai_config)

    return ChatBase(model, state, tools, helper)


def build_chat(
    model: ModelConfig,
    state: StateConfig | None = None,
    tools: ToolsConfig | None = None,
) -> ChatBase[ApiParams]:

    if model is None:
        err_msg = "no model specified!"
        raise RuntimeError
    if model.model is None:
        err_msg = "no model specified!"
        raise RuntimeError(err_msg)

    config_data = vendor_json(model.vendor)
    options_data = config_data.pop('options', {}) | parse_opts()

    api_class = config_data.get('api_cls')

    match api_class:
        case 'claude':
            return build_chat_claude(config_data, options_data, model, state, tools)
        case 'google':
            return build_chat_google(config_data, options_data, model, state, tools)
        case 'openai':
            return build_chat_openai(config_data, options_data, model, state, tools)
        case _:
            err_msg = f"api class not supported: {api_class}"
            raise RuntimeError(err_msg)


def init_state(system: str | None = None, messages: list[str] | None = None) -> StateConfig:
    return StateConfig(system, messages)


def init_tools(tools_name: str | None = None, env_name: str | None = None) -> ToolsConfig:
    if tools_name is not None and env_name is not None:
        raise ValueError

    if tools_name is None:
        if env_name is None:
            env_name = 'CHATIO_TOOLS_NAME'

        tools_name = os.environ.get(env_name)
        if not tools_name:
            tools_name = 'empty'

    tools_name, _, tool_choice = tools_name.partition(':')
    tool_choice_mode, _, tool_choice_name = tool_choice.partition(':')

    tools: dict | None = None
    match tools_name:
        case 'default':
            wiki = WikiToolFactory()

            tools = {
                "run_command": ShellExecTool(),
                "run_bc_calc": ShellCalcTool(),
                "wiki_content": wiki.wiki_content(),
                "wiki_summary": wiki.wiki_summary(),
                "wiki_section": wiki.wiki_section(),
                "wiki_search": wiki.wiki_search(),
                "web_search": WebSearchTool(),
                "web_browse": WebBrowseTool(),
                "run_nothing": DummyTool(),
            }
        case 'llmtool':
            llm = build_chat(
                model=init_model(env_name='CHATIO_NESTED_MODEL_NAME'),
                tools=init_tools(env_name='CHATIO_NESTED_TOOLS_NAME'))

            tools = {
                "llm_message": LlmDialogTool(llm),
            }
        case 'imgtool':
            tools = {
                "run_imgdump": ImageDumpTool(),
            }

    return ToolsConfig(tools, tool_choice_mode=tool_choice_mode, tool_choice_name=tool_choice_name)
