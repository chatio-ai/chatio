

from mediawiki import MediaWiki

from . import ToolBase


class WikiToolFactory:
    def __init__(self):
        self.wiki = MediaWiki()
        self.page_cache = {}

    def wiki_search(self, desc=None):
        return WikiSearchTool(self.wiki, self.page_cache, desc)

    def wiki_content(self, desc=None):
        return WikiContentTool(self.wiki, self.page_cache, desc)

    def wiki_summary(self, desc=None):
        return WikiSummaryTool(self.wiki, self.page_cache, desc)

    def wiki_section(self, desc=None):
        return WikiSectionTool(self.wiki, self.page_cache, desc)


class WikiToolBase(ToolBase):
    def __init__(self, wiki, page_cache, desc=None):
        super().__init__(desc)

        self.wiki = wiki
        self.page_cache = page_cache

    def _get_page(self, title=None):
        if not title in self.page_cache:
            title = self.wiki.suggest(title)
        if not title in self.page_cache:
            self.page_cache[title] = self.wiki.page(title, auto_suggest=False)
        return self.page_cache[title]


class WikiSearchTool(WikiToolBase):

    __desc__ = "Get list of titles based on string search"

    __schema__ = {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to search for across pages titles and content",
                },
            },
            "required": ["text"],
        }

    def __call__(self, text=None):
        return "\n".join(self.wiki.search(text))


class WikiContentTool(WikiToolBase):

    __desc__ = "Get list of sections for wikipedia article"

    __schema__ = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch list of sections for",
                },
            },
            "required": ["title"],
        }

    def __call__(self, title=None):
        return "\n".join(self._get_page(title).sections)


class WikiSummaryTool(WikiToolBase):

    __desc__ = "Get content of summary for wikipedia article"

    __schema__ = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch summary content for",
                },
            },
            "required": ["title"],
        }

    def __call__(self, title=None):
        return self._get_page(title).section(None)


class WikiSectionTool(WikiToolBase):

    __desc__ = "Get content of specific section for wikipedia article"

    __schema__ = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of article to fetch section content for",
                },
                "section": {
                    "type": "string",
                    "description": "The section name to fetch content for",
                }
            },
            "required": ["title", "section"],
        }

    def __call__(self, title=None, section=None):
        return self._get_page(title).section(section)
