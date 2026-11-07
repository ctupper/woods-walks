"""
MkDocs hook: let a list start right under a line of text.

Python-Markdown only starts a list after a blank line, so

    **Setup:** fresh folder
    - first step
    - second step

renders as one run-on paragraph ("fresh folder - first step - second
step"). GitHub and most editors render it as a list. The BMad wiki pages
are synced in from elsewhere, so instead of editing them this adds the
blank line at build time. The files on disk are not changed.
"""

import re

LIST_ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+\.)\s+\S")
FENCE = re.compile(r"^\s*(```|~~~)")


def indent_of(line):
    return len(line) - len(line.lstrip())


def on_page_markdown(markdown, **kwargs):
    lines = markdown.split("\n")
    out = []
    in_fence = False
    block = []  # the non-blank lines since the last blank line

    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence and block and LIST_ITEM.match(line):
            prev = block[-1]
            same_level = indent_of(prev) == indent_of(line)
            # Already inside a list (an earlier item, or text continuing one):
            # leave it alone
            in_list = any(
                LIST_ITEM.match(b) and indent_of(b) <= indent_of(line) for b in block
            )
            # Tables, headings and HTML end on their own; only plain text
            # swallows the list
            plain_text = not prev.lstrip().startswith(("|", "#", "<", "!!!", "???", ">"))
            if same_level and not in_list and plain_text:
                out.append("")
                block = []

        out.append(line)
        block = block + [line] if line.strip() else []

    return "\n".join(out)
