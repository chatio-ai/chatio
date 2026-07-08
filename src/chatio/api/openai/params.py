
from dataclasses import dataclass, field

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionPredictionContentParam

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat import ChatCompletionToolChoiceOptionParam

from openai import Omit, omit


@dataclass
class OpenAIParams:
    messages: list[ChatCompletionMessageParam]
    system: list[ChatCompletionMessageParam] = field(default_factory=list)
    tools: list[ChatCompletionToolParam] | Omit = omit
    tool_choice: ChatCompletionToolChoiceOptionParam | Omit = omit
    prediction: ChatCompletionPredictionContentParam | Omit = omit
