import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestGCCBenchmarkV2(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"data/gcc/benchmark.json").read_text(encoding="utf-8"))
        self.rows=self.data["countries"]

    def test_six_gcc_countries(self):
        self.assertEqual(len(self.rows),6)
        self.assertEqual({x["code"] for x in self.rows},{"SA","AE","QA","OM","BH","KW"})

    def test_sources_are_https(self):
        for row in self.rows:
            self.assertTrue(row["sources"])
            self.assertTrue(all(x.startswith("https://") for x in row["sources"]))

    def test_registry_registrar_model(self):
        self.assertTrue(all(x["registry_registrar_model"] for x in self.rows))

    def test_page_exists(self):
        html=(ROOT/"site/gcc-benchmark.html").read_text(encoding="utf-8")
        self.assertIn("GCC ccTLD Benchmark",html)

if __name__=="__main__":
    unittest.main()
