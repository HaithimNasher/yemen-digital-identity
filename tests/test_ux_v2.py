import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"site"

class TestUXV2(unittest.TestCase):
    def test_navigation_metadata(self):
        d=json.loads((ROOT/"data/ui/navigation.json").read_text(encoding="utf-8"))
        self.assertEqual(d["default_language"],"ar")
        self.assertEqual(set(d["languages"]),{"ar","en"})
        self.assertGreaterEqual(len(d["items"]),10)

    def test_i18n_files(self):
        for lang in ("ar","en"):
            p=SITE/"i18n"/f"{lang}.json"
            self.assertTrue(p.exists())
            d=json.loads(p.read_text(encoding="utf-8"))
            self.assertIn("footer",d)

    def test_shared_assets_exist(self):
        self.assertTrue((SITE/"ux-v2.css").exists())
        self.assertTrue((SITE/"ux-v2.js").exists())

    def test_all_html_pages_use_shared_ux(self):
        pages=list(SITE.glob("*.html"))
        self.assertGreaterEqual(len(pages),8)
        for p in pages:
            text=p.read_text(encoding="utf-8")
            self.assertIn("ux-v2.css",text,p.name)
            self.assertIn("ux-v2.js",text,p.name)

    def test_index_has_core_links(self):
        text=(SITE/"index.html").read_text(encoding="utf-8")
        for href in [
            "national-dashboard.html",
            "domain-search.html",
            "observatory.html",
            "policy-center.html",
            "gcc-benchmark.html"
        ]:
            self.assertIn(href,text)

    def test_accessibility_support(self):
        js=(SITE/"ux-v2.js").read_text(encoding="utf-8")
        css=(SITE/"ux-v2.css").read_text(encoding="utf-8")
        self.assertIn("ydii-skip",js)
        self.assertIn(":focus-visible",css)
        self.assertIn("prefers-reduced-motion",css)

if __name__=="__main__":
    unittest.main()
