

from mediawiki import MediaWiki

from . import ToolBase


class WikiContentTool(ToolBase):

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
        wiki = MediaWiki()
        page = wiki.page(title)

        return "\n".join(page.sections)


class WikiSummaryTool(ToolBase):

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
        wiki = MediaWiki()
        page = wiki.page(title)

        return page.section(None)


class WikiSectionTool(ToolBase):

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
        wiki = MediaWiki()
        page = wiki.page(title)

        return page.section(section)
