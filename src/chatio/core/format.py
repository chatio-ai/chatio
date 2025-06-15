
from abc import ABC, abstractmethod


class ChatFormat(ABC):

    # messages

    @abstractmethod
    def chat_messages(self, messages: list[dict]) -> list[dict]:
        ...

    @abstractmethod
    def text_chunk(self, text: str) -> dict:
        ...

    @abstractmethod
    def image_blob(self, blob: str, mimetype: str) -> dict:
        ...

    @abstractmethod
    def system_content(self, content: dict) -> dict:
        ...

    @abstractmethod
    def input_content(self, content: dict) -> dict:
        ...

    @abstractmethod
    def output_content(self, content: dict) -> dict:
        ...

    @abstractmethod
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> dict:
        ...

    @abstractmethod
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> dict:
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
