import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TestProjectData(unittest.TestCase):
    def test_gcc_dataset(self):
        data = json.loads((ROOT / "data/gcc_domains.json").read_text(encoding="utf-8"))
        cc = {x["ccTLD"] for x in data["countries"]}
        self.assertTrue({".sa",".ae",".qa",".kw",".om",".bh",".ye"}.issubset(cc))

    def test_sources_are_https(self):
        data = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["sources"]), 8)
        self.assertTrue(all(x["url"].startswith("https://") for x in data["sources"]))

    def test_site_exists(self):
        html = (ROOT / "site/index.html").read_text(encoding="utf-8")
        self.assertIn("Yemen Digital Identity", html)
        self.assertIn(".ye", html)

if __name__ == "__main__":
    unittest.main()
