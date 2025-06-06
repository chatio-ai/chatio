
from typing import override

from googlesearch import search, get

from html2text import html2text

from . import ToolBase


class WebSearchTool(ToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Peform web search for given search string. Returns up to 10 urls each on separate line."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to search for",
                },
            },
            "required": ["text"],
        }

    def __call__(self, text=None):
        yield "\n".join(search(text))


class WebBrowseTool(ToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Perform web browse for given url. Returns content of the given url in markdown format."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url to get content for",
                },
            },
            "required": ["url"],
        }

    def __call__(self, url=None):
        yield html2text(get(url, timeout=10).text)
