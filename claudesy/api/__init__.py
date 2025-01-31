


class ChatBase:

    def __init__(self, system=None, messages=None, tools=None, tool_choice=None, tool_choice_name=None, model=None, **kwargs):

        self._setup_context(model, **kwargs)

        self._setup_messages(system, messages)

        self._setup_tools(tools, tool_choice, tool_choice_name)

    def _setup_context(self, model, **kwargs):
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



