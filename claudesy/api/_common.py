
import json


class ChatConfig:

    def __init__(self, configpath=None):
        self._config = self._fromfile(configpath)

        self.model = self._config.get('model')
        self.api_key = self._config.get('api_key')
        self.api_url = self._config.get('api_url')
        self.api_type = self._config.get('api_type')

    def _validate(self):
        pass

    def _fromfile(self, configpath):
        if configpath is None:
            return {}

        try:
            with open(configpath, 'r') as configfp:
                return json.load(configfp)
        except FileNotFoundError:
            return {}


class ChatBase:

    def __init__(self, system=None, messages=None, tools=None, tool_choice=None, tool_choice_name=None, model=None, config: ChatConfig = None, **kwargs):

        if config is None:
            config = ChatConfig()
        if model is not None:
            config.model = model
        if config.model is None:
            raise RuntimeError()

        self._setup_context(config, **kwargs)

        self._setup_messages(system, messages)

        self._setup_tools(tools, tool_choice, tool_choice_name)

    def _setup_context(self, config, **kwargs):
        raise NotImplementedError()

    def _setup_messages(self, system, messages):
        raise NotImplementedError()

    def _setup_tools(self, tools, tool_choice, tool_choice_name):
        raise NotImplementedError()

    def _as_contents(self, content):
        if isinstance(content, str):
            return [{"type": "text", "text": content}]
        else:
            return content

    def _usr_message(self, content):
        return {"role": "user", "content": self._as_contents(content)}

    def _bot_message(self, content):
        return {"role": "assistant", "content": self._as_contents(content)}



