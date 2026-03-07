"""
Markdown Link Prefix: Python-Markdown extension for prefixed link shorthand.

Expands links like [text](youtube:VIDEO_ID) or [text](snkb:KB123) into
full URLs using configurable prefix → URL templates. Easy to add new prefixes.
"""

from markdown_link_prefix.extension import LinkPrefixExtension, make_extension

# Python-Markdown discovers extensions via makeExtension (camelCase)
makeExtension = make_extension

__all__ = ["LinkPrefixExtension", "make_extension", "makeExtension"]
