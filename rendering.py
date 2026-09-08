"""Markdown rendering shared by the static builder and its checks."""
from markdown_it import MarkdownIt

_parser = MarkdownIt('commonmark', {'html': False}).enable(['table', 'strikethrough'])

def markdown(text):
    return _parser.render(text)
