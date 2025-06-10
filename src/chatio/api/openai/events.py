
import logging

from collections.abc import Iterator


from openai.lib.streaming.chat._completions import ChatCompletionStreamManager


from chatio.core.events import ChatEvent, TextEvent, DoneEvent, StatEvent, CallEvent


log = logging.getLogger(__name__)


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
            if not isinstance(call.function.parsed_arguments, dict):
                raise TypeError(call.function.parsed_arguments)
            yield CallEvent(call.id, call.function.name,
                            call.function.parsed_arguments, call.function.arguments)
