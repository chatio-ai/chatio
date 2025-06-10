
import logging

from collections.abc import Iterator

from dataclasses import dataclass

from typing import override

from httpx import Client as HttpxClient

from openai import OpenAI
from openai.lib.streaming.chat._completions import ChatCompletionStreamManager


from chatio.core.events import ChatEvent, TextEvent, DoneEvent, StatEvent, CallEvent

from ._utils import httpx_args

from ._common import ApiConfig
from ._common import ApiParams
from ._common import ChatBase


log = logging.getLogger(__name__)


@dataclass
class OpenAIParams(ApiParams):
    prediction: bool = False
    legacy: bool = False


def _pump(streamctx: ChatCompletionStreamManager) -> Iterator[ChatEvent]:
    with streamctx as stream:
        for chunk in stream:
            log.info("%s", chunk.model_dump_json(indent=2))

            if chunk.type == 'content.delta':
                yield TextEvent(chunk.delta)

        final = stream.get_final_completion()
        final_message = final.choices[0].message
        yield DoneEvent(final_message.content or "")

        usage = final.usage

        input_details = usage and usage.prompt_tokens_details
        output_details = usage and usage.completion_tokens_details

        yield StatEvent(
            (usage and usage.prompt_tokens) or 0,
            (usage and usage.completion_tokens) or 0,
            0,
            (input_details and input_details.cached_tokens) or 0,
            (output_details and output_details.accepted_prediction_tokens) or 0,
            (output_details and output_details.rejected_prediction_tokens) or 0,
        )

        for call in final_message.tool_calls or ():
            yield CallEvent(call.id, call.function.name,
                            call.function.parsed_arguments, call.function.arguments)


class OpenAIChat(ChatBase):

    @override
    def _setup_context(self, config: ApiConfig):
        self._client = OpenAI(
            base_url=config.api_url,
            api_key=config.api_key,
            http_client=HttpxClient(**httpx_args()))

        self._params = OpenAIParams(**config.options if config.options else {})

    # tools

    def _tool_schema(self, schema):
        result = schema.copy()

        props = None
        if result.get("type") == "object":
            props = result.setdefault("properties", {})

        if props is not None:
            result.update({
                "additionalProperties": False,
                "required": list(props),
            })

            for key in props:
                value = props.get(key, {})
                value = self._tool_schema(value)
                props[key] = value

        return result

    @override
    def _format_tool_definition(self, name, desc, schema):
        schema = self._tool_schema(schema)
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": schema,
                "strict": True,
            },
        }

    @override
    def _format_tool_selection(self, tool_choice, tool_choice_name):
        if not tool_choice:
            return None

        if not tool_choice_name:
            return {"type": tool_choice}

        return {"type": tool_choice, "function": {"name": tool_choice_name}}

    # messages

    @override
    def _format_text_chunk(self, text):
        if self._params.legacy:
            return text
        return {"type": "text", "text": text}

    @override
    def _format_image_blob(self, blob, mimetype):
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mimetype};base64,{blob}"},
        }

    @override
    def _format_dev_message(self, content):
        if not content:
            return [], []

        return [], [{
            "role": "developer",
            "content": self._as_contents(content),
        }]

    @override
    def _format_user_message(self, content):
        return {
            "role": "user",
            "content": self._as_contents(content),
        }

    @override
    def _format_model_message(self, content):
        return {
            "role": "assistant",
            "content": self._as_contents(content),
        }

    @override
    def _format_tool_request(self, tool_call_id, tool_name, tool_input):
        return {
            "role": "assistant",
            "tool_calls": [{
                "id": tool_call_id,
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": tool_input,
                },
            }],
        }

    @override
    def _format_tool_response(self, tool_call_id, tool_name, tool_output):
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_output,
        }

    def _format_predict_content(self, prediction):
        return {
            "type": "content",
            "content": prediction,
        }

    # events

    def _iterate_model_events_prediction(self, model, _system, messages, prediction) -> Iterator[ChatEvent]:
        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            stream_options={'include_usage': True},
            messages=messages,
            prediction=prediction))

    @override
    def _iterate_model_events(self, model, system, messages, tools, **kwargs) -> Iterator[ChatEvent]:
        prediction = kwargs.pop('prediction', None)
        if self._params.prediction and prediction:
            prediction = self._format_predict_content(prediction)
            return self._iterate_model_events_prediction(model, system, messages, prediction)

        return _pump(self._client.beta.chat.completions.stream(
            model=model,
            max_completion_tokens=4096,
            stream_options={'include_usage': True},
            tools=tools,
            messages=messages))

    @override
    def _count_message_tokens(self, model, system, messages, tools):
        raise NotImplementedError
