
from collections.abc import Callable

from typing import override

from mediawiki import MediaWiki, MediaWikiPage

from . import ToolBase


class WikiToolFactory:
    def __init__(self):
        self.wiki = MediaWiki()
        self.page_cache = {}

    def wiki_search(self):
        return WikiSearchTool(self.wiki)

    def wiki_content(self):
        return WikiContentTool(self.wiki, self.page_cache)

    def wiki_summary(self):
        return WikiSummaryTool(self.wiki, self.page_cache)

    def wiki_section(self):
        return WikiSectionTool(self.wiki, self.page_cache)


class WikiPageToolBase(ToolBase):
    def __init__(self, wiki, page_cache):
        self.wiki = wiki
        self.page_cache = page_cache

    def _get_page(self, title: str | None) -> tuple[MediaWikiPage | None, bool | None]:
        cached = title in self.page_cache
        if not cached:
            title = self.wiki.suggest(title)

        if title is None:
            return None, None

        cached = cached or title in self.page_cache
        if not cached:
            self.page_cache[title] = self.wiki.page(title, auto_suggest=False)

        return self.page_cache[title], cached

    def _page_do(self, title: str | None, func: Callable[[MediaWikiPage], object]):
        page, cached = self._get_page(title)
        yield {"title": title, "cache": cached}

        if page is not None:
            yield func(page)


class WikiSearchTool(ToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Get list of titles based on string search. Returns up to 10 titles each on separate line."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to search for across pages titles and content.",
                },
            },
            "required": ["text"],
        }

    def __init__(self, wiki):
        self.wiki = wiki

    def __call__(self, text=None):
        yield "\n".join(self.wiki.search(text))


class WikiContentTool(WikiPageToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Get list of sections for wikipedia article. Returns list of sections each on separate line."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch list of sections for.",
                },
            },
            "required": ["title"],
        }

    def __call__(self, title: str | None = None):
        return self._page_do(title, lambda page: "\n".join(page.sections))


class WikiSummaryTool(WikiPageToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Get content of summary for wikipedia article. Returns text of summary (header) section."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch summary content for.",
                },
            },
            "required": ["title"],
        }

    def __call__(self, title: str | None = None):
        return self._page_do(title, lambda page: page.section(None))


class WikiSectionTool(WikiPageToolBase):

    @staticmethod
    @override
    def desc() -> str:
        return "Get content of specific section for wikipedia article. Returns text of the given section."

    @staticmethod
    @override
    def schema() -> dict[str, object]:
        return {
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

    def __call__(self, title: str | None = None, section: str | None = None):
        return self._page_do(title, lambda page: page.section(section))
