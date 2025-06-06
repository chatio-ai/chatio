

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
        cached = True
        if title not in self.page_cache:
            title = self.wiki.suggest(title)
        if title not in self.page_cache:
            self.page_cache[title] = self.wiki.page(title, auto_suggest=False)
            cached = False
        return self.page_cache[title], cached

    def _run_tool(self, page=None, **kwargs):
        raise NotImplementedError()

    def __call__(self, title=None, **kwargs):
        page, cached = self._get_page(title)
        yield {"title": title, "cache": cached}
        yield from self._run_tool(page, **kwargs)


class WikiSearchTool(WikiToolBase):

    __desc__ = "Get list of titles based on string search. Returns up to 10 titles each on separate line."

    __schema__ = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to search for across pages titles and content.",
            },
        },
        "required": ["text"],
    }

    def __call__(self, text=None):
        yield "\n".join(self.wiki.search(text))


class WikiContentTool(WikiToolBase):

    __desc__ = "Get list of sections for wikipedia article. Returns list of sections each on separate line."

    __schema__ = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of article to fetch list of sections for.",
            },
        },
        "required": ["title"],
    }

    def _run_tool(self, page=None):
        yield "\n".join(page.sections)


class WikiSummaryTool(WikiToolBase):

    __desc__ = "Get content of summary for wikipedia article. Returns text of summary (header) section."

    __schema__ = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of article to fetch summary content for.",
            },
        },
        "required": ["title"],
    }

    def _run_tool(self, page=None):
        yield page.section(None)


class WikiSectionTool(WikiToolBase):

    __desc__ = "Get content of specific section for wikipedia article. Returns text of the given section."

    __schema__ = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of article to fetch section content for.",
            },
            "section": {
                "type": "string",
                "description": "The section name to fetch content for.",
            }
        },
        "required": ["title", "section"],
    }

    def _run_tool(self, page=None, section=None):
        yield page.section(section)
