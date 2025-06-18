
from abc import ABC, abstractmethod


class ApiFormat[
    SystemContent,
    MessageContent,
    PredictionContent,
    TextMessage,
    ImageMessage,
    ToolDefinition,
    ToolDefinitions,
    ToolSelection,
](ABC):

    # messages

    @abstractmethod
    def chat_messages(self, messages: list[MessageContent]) -> list[MessageContent]:
        ...

    @abstractmethod
    def text_chunk(self, text: str) -> TextMessage:
        ...

    @abstractmethod
    def image_blob(self, blob: bytes, mimetype: str) -> ImageMessage:
        ...

    @abstractmethod
    def system_content(self, content: TextMessage) -> SystemContent:
        ...

    @abstractmethod
    def prediction_content(self, content: TextMessage) -> PredictionContent | None:
        ...

    @abstractmethod
    def input_content(self, content: TextMessage | ImageMessage) -> MessageContent:
        ...

    def input_message(self, message: str) -> MessageContent:
        return self.input_content(self.text_chunk(message))

    @abstractmethod
    def output_content(self, content: TextMessage | ImageMessage) -> MessageContent:
        ...

    def output_message(self, message: str) -> MessageContent:
        return self.output_content(self.text_chunk(message))

    @abstractmethod
    def call_request(self, tool_call_id: str, tool_name: str, tool_input: object) -> MessageContent:
        ...

    @abstractmethod
    def call_response(self, tool_call_id: str, tool_name: str, tool_output: str) -> MessageContent:
        ...

    def image_document(self, blob: bytes, mimetype: str) -> MessageContent:
        return self.input_content(self.image_blob(blob, mimetype))

    # functions

    @abstractmethod
    def tool_definition(self, name: str, desc: str, schema: dict) -> ToolDefinition:
        ...

    @abstractmethod
    def tool_definitions(self, tools: list[ToolDefinition]) -> ToolDefinitions | None:
        ...

    @abstractmethod
    def tool_selection_none(self) -> ToolSelection | None:
        ...

    @abstractmethod
    def tool_selection_auto(self) -> ToolSelection | None:
        ...

    @abstractmethod
    def tool_selection_any(self) -> ToolSelection | None:
        ...

    @abstractmethod
    def tool_selection_name(self, tool_name: str) -> ToolSelection | None:
        ...
