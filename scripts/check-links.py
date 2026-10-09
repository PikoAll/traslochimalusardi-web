#!/usr/bin/env python3
"""Check local references of root *.html pages and sitemap.xml URLs.

Usage: python3 scripts/check-links.py [ROOT]
Exit 0 if everything resolves, 1 otherwise (prints `file.html -> path`).
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ATTR_RE = re.compile(r'\b(?:href|src)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.I)
SKIP_PREFIXES = ("http://", "https://", "tel:", "mailto:", "#", "//", "data:", "javascript:")


def local_path(ref):
    """Return the file path of a local reference, or None if it must be ignored."""
    ref = ref.strip()
    if not ref or ref.lower().startswith(SKIP_PREFIXES):
        return None
    path = re.split(r"[?#]", ref, maxsplit=1)[0]
    return path or None


def check_pages(root):
    errors = []
    for page in sorted(root.glob("*.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        for m in ATTR_RE.finditer(text):
            path = local_path(m.group(1) if m.group(1) is not None else m.group(2))
            if path is None:
                continue
            target = root / path.lstrip("/")
            if not target.exists():
                errors.append("%s -> %s" % (page.name, path))
    return errors


def check_sitemap(root):
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        return []
    errors = []
    for el in ET.parse(sitemap).getroot().iter():
        if el.tag.endswith("}loc") or el.tag == "loc":
            path = urlparse((el.text or "").strip()).path.lstrip("/")
            page = path or "index.html"
            if not page.endswith(".html") or not (root / page).is_file():
                errors.append("sitemap.xml -> %s" % page)
    return errors


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    errors = check_pages(root) + check_sitemap(root)
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
