
import asyncio

from abc import ABC, abstractmethod

from collections.abc import AsyncIterator

from typing import override

from googlesearch import search as googlesearch, get
from googlesearch import SearchResult

from html2text import html2text

from chatio.core.schema import ToolSchemaDict
from chatio.core.invoke import ToolBase


class WebSearchToolBase(ToolBase, ABC):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "web_search",
            "description":
                "Peform web search for given text. Returns up to 10 urls each on separate line.",
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to search for",
                },
            },
            "required": ["text"],
        }

    @abstractmethod
    def __call__(self, text: str) -> AsyncIterator[str]:
        ...


class GoogleSearchTool(WebSearchToolBase):

    def _result_to_str(self, result: str | SearchResult) -> str:
        return result if isinstance(result, str) else result.url

    @override
    # pylint: disable=invalid-overridden-method
    async def __call__(self, text: str) -> AsyncIterator[str]:
        results = await asyncio.to_thread(lambda: list(googlesearch(text)))
        yield "\n".join(self._result_to_str(result) for result in results)


class WebBrowseTool(ToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "web_browse",
            "description":
                "Perform web browse for given url. Returns content of the given url in md format.",
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url to get content for",
                },
            },
            "required": ["url"],
        }

    @override
    # pylint: disable=invalid-overridden-method
    async def __call__(self, url: str) -> AsyncIterator[str]:
        text = await asyncio.to_thread(lambda: get(url, timeout=10).text)
        yield html2text(text)
