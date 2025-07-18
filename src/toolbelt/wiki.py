
from collections.abc import Iterator
from collections.abc import Callable

from typing import override

from mediawiki import MediaWiki, MediaWikiPage

from . import ToolSchemaDict
from . import ToolBase


# pylint: disable=too-few-public-methods
class WikiPageToolBase(ToolBase):
    def __init__(self, wiki: MediaWiki, page_cache: dict[str, MediaWikiPage]) -> None:
        self.wiki = wiki
        self.page_cache = page_cache

    def _get_page(self, title: str | None) -> tuple[MediaWikiPage, bool] | None:
        cached = title in self.page_cache
        if not cached:
            title = self.wiki.suggest(title)

        if title is None:
            return None

        cached = cached or title in self.page_cache
        if not cached:
            self.page_cache[title] = self.wiki.page(title, auto_suggest=False)

        return self.page_cache[title], cached

    def _page_do(self, title: str | None, func: Callable[[MediaWikiPage], str | None]) -> Iterator[str | dict]:
        page_entry = self._get_page(title)
        if page_entry is None:
            yield {"title": title, "cache": None}
            return

        page, cached = page_entry
        yield {"title": title, "cache": cached}

        data = func(page)
        if data is not None:
            yield data


class WikiSearchTool(ToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "wiki_search",
            "description": "Search wiki pages for given text. Returns up to 10 titles each on separate line.",
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The term to search for across pages titles and content.",
                },
            },
            "required": ["text"],
        }

    def __init__(self, wiki) -> None:
        self.wiki = wiki

    @override
    def __call__(self, text=None) -> Iterator[str | dict]:
        yield "\n".join(self.wiki.search(text))


class WikiContentTool(WikiPageToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "wiki_content",
            "description": "Get list of wiki page sections. Returns list of sections each on separate line.",
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch list of sections for.",
                },
            },
            "required": ["title"],
        }

    @override
    def __call__(self, title: str | None = None) -> Iterator[str | dict]:
        return self._page_do(title, lambda page: "\n".join(page.sections))


class WikiSummaryTool(WikiPageToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "wiki_summary",
            "description": "Get content of wiki page summary. Returns text of summary (header) section.",
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch summary content for.",
                },
            },
            "required": ["title"],
        }

    @override
    def __call__(self, title: str | None = None) -> Iterator[str | dict]:
        return self._page_do(title, lambda page: page.section(None))


class WikiSectionTool(WikiPageToolBase):

    @staticmethod
    @override
    def schema() -> ToolSchemaDict:
        return {
            "name": "wiki_section",
            "description": "Get content of wiki page section. Returns text of the given section.",
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch section content for.",
                },
                "section": {
                    "type": "string",
                    "description": "The section name to fetch content for.",
                },
            },
            "required": ["title", "section"],
        }

    @override
    def __call__(self, title: str | None = None, section: str | None = None) -> Iterator[str | dict]:
        return self._page_do(title, lambda page: page.section(section))


class WikiToolFactory:
    def __init__(self) -> None:
        self.wiki = MediaWiki()
        self.page_cache: dict[str, MediaWikiPage] = {}

    def wiki_search(self) -> WikiSearchTool:
        return WikiSearchTool(self.wiki)

    def wiki_content(self) -> WikiContentTool:
        return WikiContentTool(self.wiki, self.page_cache)

    def wiki_summary(self) -> WikiSummaryTool:
        return WikiSummaryTool(self.wiki, self.page_cache)

    def wiki_section(self) -> WikiSectionTool:
        return WikiSectionTool(self.wiki, self.page_cache)
