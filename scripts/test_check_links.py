"""Tests for scripts/check-links.py (TRM-001).

Contract assumed: `python3 scripts/check-links.py [ROOT]` -- ROOT defaults to the
repo root (parent of scripts/); exit 0 if ok, 1 otherwise, printing
`file.html -> path` for each missing reference.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check-links.py"

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>"""


def url(loc):
    return "<url><loc>%s</loc></url>" % loc


class CheckLinksTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def run_check(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.root)],
            capture_output=True, text=True,
        )

    def base_site(self):
        self.write("index.html",
                   '<link href="assets/css/main.css"><script src="assets/js/a.js"></script>'
                   '<a href="chi-siamo.html">x</a>')
        self.write("chi-siamo.html", "<p>hi</p>")
        self.write("assets/css/main.css", "")
        self.write("assets/js/a.js", "")
        self.write("sitemap.xml", SITEMAP % (
            url("https://example.com/") + url("https://example.com/chi-siamo.html")))

    def test_all_ok_exits_zero(self):
        self.base_site()
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_reference_exits_one_and_reports(self):
        self.base_site()
        self.write("index.html", '<img src="images/missing.jpg">')
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("index.html -> images/missing.jpg", r.stdout)

    def test_each_missing_reference_reported(self):
        self.base_site()
        self.write("index.html", '<a href="a.html">a</a><img src="b.png">')
        r = self.run_check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("index.html -> a.html", r.stdout)
        self.assertIn("index.html -> b.png", r.stdout)

    def test_query_string_is_ignored(self):
        self.base_site()
        self.write("index.html", '<link href="assets/css/main.css?v=123">')
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_query_string_missing_file_reported_without_query(self):
        self.base_site()
        self.write("index.html", '<link href="assets/css/nope.css?v=9">')
        r = self.run_check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("index.html -> assets/css/nope.css", r.stdout)
        self.assertNotIn("?v=9", r.stdout)

    def test_external_and_special_links_ignored(self):
        self.base_site()
        self.write("index.html",
                   '<a href="http://x.it/a">1</a><a href="https://x.it/b">2</a>'
                   '<a href="tel:+390123">3</a><a href="mailto:a@b.it">4</a>'
                   '<a href="#top">5</a>')
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_leading_slash_is_relative_to_root(self):
        self.base_site()
        self.write("index.html", '<link href="/assets/css/main.css">')
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_sitemap_url_without_page_fails(self):
        self.base_site()
        self.write("sitemap.xml", SITEMAP % (
            url("https://example.com/") + url("https://example.com/fantasma.html")))
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("fantasma.html", r.stdout)

    def test_known_missing_reference_is_tolerated(self):
        self.base_site()
        self.write("index.html", '<img src="images/missing.jpg">')
        self.write("scripts/check-links.known",
                   "# baseline\nindex.html -> images/missing.jpg\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_new_missing_reference_still_fails_with_baseline(self):
        self.base_site()
        self.write("index.html", '<img src="images/missing.jpg"><img src="images/new.jpg">')
        self.write("scripts/check-links.known", "index.html -> images/missing.jpg\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("index.html -> images/new.jpg", r.stdout)
        self.assertNotIn("images/missing.jpg", r.stdout)

    def test_sitemap_root_maps_to_index(self):
        self.base_site()
        (self.root / "index.html").rename(self.root / "home.html")
        self.write("sitemap.xml", SITEMAP % url("https://example.com/"))
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
