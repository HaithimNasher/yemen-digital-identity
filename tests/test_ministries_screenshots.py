import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestMinistriesScreenshots(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"data/entities/ministries.json").read_text(encoding="utf-8"))
        self.rows=self.data["entities"]

    def test_count(self):
        self.assertEqual(len(self.rows),26)

    def test_domains_unique(self):
        domains=[x["current_domain"] for x in self.rows]
        self.assertEqual(len(domains),len(set(domains)))

    def test_required_domains(self):
        domains={x["current_domain"] for x in self.rows}
        for d in ["moi.gov.ye","mod.gov.ye","mofa.gov.ye","mof.gov.ye","moe.gov.ye","moh.gov.ye","minfo.gov.ye"]:
            self.assertIn(d,domains)

    def test_screenshot_status(self):
        self.assertTrue(all(x["verification_status"]=="screenshot-reference" for x in self.rows))

if __name__=="__main__":
    unittest.main()
