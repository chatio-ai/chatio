
import logging

from collections.abc import Iterator
from collections.abc import Callable


from google.genai.types import GenerateContentResponse
from google.genai.types import GroundingMetadata

from html2text import HTML2Text


from chatio.core.events import ChatEvent, CallEvent, DoneEvent, StatEvent, TextEvent


log = logging.getLogger(__name__)


def _pump_grounding(search: GroundingMetadata | None) -> Iterator[ChatEvent]:
    if search is None:
        return

    if search.grounding_chunks is not None:
        for index, chunk in enumerate(search.grounding_chunks, 1):
            uri, title = "", ""
            if chunk.web is not None and chunk.web.uri is not None:
                uri = chunk.web.uri
            if chunk.web is not None and chunk.web.title is not None:
                title = chunk.web.title
            entry = f"   [{index}]: <{uri}> {title}\n"
            yield TextEvent(entry, label="search.sources")

    if search.search_entry_point is not None:
        parser = HTML2Text(bodywidth=0)
        parser.inline_links = False
        parser.protect_links = True
        entry = parser.handle(search.search_entry_point.rendered_content or "")
        yield TextEvent(entry, label="search.suggest")


def _pump(streamfun: Callable[[], Iterator[GenerateContentResponse]]) -> Iterator[ChatEvent]:
    stream = streamfun()

    if stream is not None:

        usage = None
        calls = []
        final_text = ""
        search = None

        for chunk in stream:
            log.info("%s", chunk.model_dump_json(indent=2))

            if chunk.candidates \
                    and chunk.candidates[0].content \
                    and chunk.candidates[0].content.parts:

                for part in chunk.candidates[0].content.parts:
                    if part.text:
                        final_text += part.text
                        yield TextEvent(part.text)

                    if part.function_call:
                        calls.append(part.function_call)

                usage = chunk.usage_metadata
                search = chunk.candidates[0].grounding_metadata

        for event in _pump_grounding(search):
            if event is not None:
                yield event

        yield DoneEvent(final_text)

        yield StatEvent(
            (usage and usage.prompt_token_count) or 0,
            (usage and usage.candidates_token_count) or 0,
            0, (usage and usage.cached_content_token_count) or 0,
            0, 0)

        for call in calls:
            yield CallEvent(call.id or "", call.name or "", call.args, call.args)
