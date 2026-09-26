import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestNationalDirectoryV2(unittest.TestCase):
    def setUp(self):
        self.u=json.loads((ROOT/"data/entities/universities.json").read_text(encoding="utf-8"))
        self.m=json.loads((ROOT/"data/entities/ministries.json").read_text(encoding="utf-8"))

    def test_university_count(self):
        self.assertEqual(len(self.u["entities"]),21)

    def test_ministries_preserved(self):
        self.assertEqual(len(self.m["entities"]),26)

    def test_university_domains_are_proposed(self):
        self.assertTrue(all(x["domain_status"]=="PROPOSED" for x in self.u["entities"]))

    def test_unique_university_ids(self):
        ids=[x["id"] for x in self.u["entities"]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_directory_page_exists(self):
        html=(ROOT/"site/directory.html").read_text(encoding="utf-8")
        self.assertIn("National Entity Directory",html)

if __name__=="__main__":
    unittest.main()
