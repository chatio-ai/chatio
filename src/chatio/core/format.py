
from abc import ABC, abstractmethod


class ChatFormat(ABC):

    @abstractmethod
    def chat_messages(self, messages: list[dict]) -> list[dict]:
        ...

    @abstractmethod
    def text_chunk(self, text: str) -> dict:
        ...

    @abstractmethod
    def image_blob(self, blob: str, mimetype: str) -> dict:
        ...

    # messages

    def _as_contents(self, content: list[dict] | dict | str) -> list[dict]:
        match content:
            case str():
                return [self.text_chunk(content)]
            case dict():
                return [content]
            case list():
                return content
            case _:
                raise RuntimeError

    @abstractmethod
    def system_message(self, content: str | None) -> tuple[list[dict] | dict | None, list[dict]]:
        ...

    @abstractmethod
    def input_message(self, content: str) -> dict:
        ...

    @abstractmethod
    def output_message(self, content: str) -> dict:
        ...

    @abstractmethod
    def tool_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> dict:
        ...

    @abstractmethod
    def tool_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> dict:
        ...

    # functions

    @abstractmethod
    def tool_definition(self, name: str, desc: str, schema: dict) -> dict:
        ...

    @abstractmethod
    def tool_definitions(self, tools: list[dict]) -> list[dict] | None:
        ...

    @abstractmethod
    def tool_selection(self, tool_choice: str | None, tool_choice_name: str | None) -> dict | None:
        ...
