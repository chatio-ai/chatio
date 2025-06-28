
from typing import override

from googlesearch import search, get

from html2text import html2text

from . import ToolBase


class WebSearchTool(ToolBase):

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "name": "web_search",
            "description": "Peform web search for given text. Returns up to 10 urls each on separate line.",
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to search for",
                },
            },
            "required": ["text"],
        }

    def _result_to_str(self, result):
        return result if isinstance(result, str) else result.url

    def __call__(self, text: str):
        yield "\n".join(self._result_to_str(result) for result in search(text))


class WebBrowseTool(ToolBase):

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "name": "web_browse",
            "description": "Perform web browse for given url. Returns content of the given url in md format.",
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url to get content for",
                },
            },
            "required": ["url"],
        }

    def __call__(self, url: str):
        yield html2text(get(url, timeout=10).text)
