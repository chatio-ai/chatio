
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

    def __init__(self,
                 system=None, messages=None,
                 tools=None, tool_choice=None, tool_choice_name=None,
                 config: ChatConfig = None, **kwargs):

        self._setup_context(config, **kwargs)

        self._setup_messages(system, messages)

        self._setup_tools(tools, tool_choice, tool_choice_name)

    def _setup_context(self, config: ChatConfig, **kwargs):
        raise NotImplementedError()

    def _setup_tools(self, tools, tool_choice, tool_choice_name):
        raise NotImplementedError()

    # messages

    def _setup_messages(self, system, messages):
        self._messages = []

        self._commit_dev_message(system)

        if messages is None:
            messages = []

        for index, message in enumerate(messages):
            if not index % 2:
                self._commit_user_message(message)
            else:
                self._commit_model_message(message)

    def _format_dev_message(self, content):
        raise NotImplementedError()

    def _commit_dev_message(self, content):
        self._messages.append(self._format_dev_message(content))

    def _format_user_message(self, content):
        raise NotImplementedError()

    def _commit_user_message(self, content):
        self._messages.append(self._format_user_message(content))

    def _format_model_message(self, content):
        raise NotImplementedError()

    def _commit_model_message(self, content):
        self._messages.append(self._format_model_message(content))

    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        raise NotImplementedError()

    def _commit_tool_request(self, tool_call_id, tool_name, tool_input):
        self._messages.append(self._format_tool_request(tool_call_id, tool_name, tool_input))

    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        raise NotImplementedError()

    def _commit_tool_response(self, tool_call_id, tool_name, tool_output):
        self._messages.append(self._format_tool_response(tool_call_id, tool_name, tool_output))

    # tools

    def _process_tool(self, tool_name, tool_args):
        func = self._funcs.get(tool_name)
        if func is not None:
            yield from func(**tool_args)

    def _process_tools(self, tool_calls):
        for tool_call in tool_calls:
            tool_call_id, tool_name, tool_input = tool_call

            content_chunks = []
            for chunk in self._process_tool(tool_name, tool_input):
                if isinstance(chunk, str):
                    content_chunks.append(chunk)
                    yield chunk
                elif chunk is not None:
                    yield {
                        "type": "tools_event",
                        "tool_name": tool_name,
                        "tool_data": chunk,
                    }

            self._commit_tool_response(tool_call_id, tool_name, "".join(content_chunks))
