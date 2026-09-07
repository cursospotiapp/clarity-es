#!/usr/bin/env python3
"""
strip_markdown.py — extrae la prosa visible de un borrador Markdown.

Elimina frontmatter YAML, bloques de código, imágenes, comentarios HTML, tablas y
marcas de títulos, listas, citas y énfasis. Conserva el texto de los enlaces y del
código en línea; descarta los destinos de los enlaces. Es una extracción heurística,
no un parser Markdown completo. No modifica el archivo fuente.

Uso:
    python3 strip_markdown.py draft.md > draft.txt
    python3 strip_markdown.py draft.md | python3 prose_stats.py -
"""

import re
import sys


def strip(text):
    text = text.lstrip('\ufeff').replace('\r\n', '\n')
    # YAML frontmatter
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    # HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    # Fenced code
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    text = re.sub(r"^~~~.*?^~~~", "", text, flags=re.S | re.M)
    # Indented code blocks
    text = re.sub(r"^(?: {4}|\t).*$", "", text, flags=re.M)
    # Images before links, so alt text goes with the image
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    # Links: keep the text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", text)
    # Reference definitions
    text = re.sub(r"^\s*\[[^\]]+\]:\s+\S+.*$", "", text, flags=re.M)
    # Inline code
    text = re.sub(r"`+([^`]*)`+", r"\1", text)
    # Tables
    text = re.sub(r"^\s*\|.*$", "", text, flags=re.M)
    # Horizontal rules
    text = re.sub(r"^\s*(?:[-*_]\s*){3,}$", "", text, flags=re.M)
    # Headings, blockquotes, list markers
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"^\s{0,3}>\s?", "", text, flags=re.M)
    text = re.sub(r"^\s{0,3}(?:[-*+]|\d+\.)\s+", "", text, flags=re.M)
    # Emphasis marks
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"(?<![\w_])_([^_]+)_(?![\w_])", r"\1", text)
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    # Residual HTML tags
    text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)
    # Collapse blank runs
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main():
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        text = sys.stdin.read()
    else:
        with open(sys.argv[1], encoding="utf-8-sig") as fh:
            text = fh.read()
    sys.stdout.write(strip(text))


if __name__ == "__main__":
    main()
