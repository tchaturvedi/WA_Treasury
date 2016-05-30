from markdown.inlinepatterns import SimpleTagPattern
from markdown.extensions import Extension

# Global Vars
MARK_RE =r'(\?{3}|_{3})(.*?)(\?{3}|_{3})'

class HighlightExtension(Extension):
    """Adds MARK_RE extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """Modifies inline patterns."""
        mark_tag = SimpleTagPattern(MARK_RE, 'mark')
        md.inlinePatterns.add('mark', mark_tag, '_begin')



def makeExtension(configs=None):
    return HighlightExtension(configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()